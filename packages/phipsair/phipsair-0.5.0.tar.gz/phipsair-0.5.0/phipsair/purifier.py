"""persistent provides a reliable client for Philips Air Purifiers."""
from __future__ import annotations

import asyncio
import enum
import logging
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Union

from phipsair import CoAPClient

_LOGGER = logging.getLogger(__name__)


@enum.unique
class Mode(enum.Enum):
    """
    Mode represents the purifier operation modes.

    The modes define how speed is controlled by the purifier itself. Only Sleep mode
    also turns off lights on the device.

    The values are the values exposed by the device's JSON API, for convenience when converting
    the JSON.
    """

    Manual = "M"
    Auto = "P"
    Allergen = "A"
    Sleep = "S"
    BacteriaVirus = "B"


@enum.unique
class FanSpeed(enum.Enum):
    """
    FanSpeed represents the different fan speeds reported by the device.

    The values are the values exposed by the device's JSON API, for convenience when converting
    the JSON.
    """

    Off = "0"
    Silent = "s"
    Speed1 = "1"
    Speed2 = "2"
    Speed3 = "3"
    Turbo = "t"


class Status:
    """Status represents the air purifier status in a form easily usable by the fan entity."""

    def __init__(
        self,
        device_id: str,
        name: str,
        model: str,
        firmware_version: str,
        wifi_firmware_version: str,
        is_on: bool,
        mode: Mode,
        fan_speed: FanSpeed,
    ) -> None:
        """
        Create a new status from the given attributes.

        The attributes are usually extracted from the JSON provided by the purifier.
        """
        self.device_id = device_id
        self.name = name
        self.model = model
        self.firmware_version = firmware_version
        self.wifi_firmware_version = wifi_firmware_version
        self.is_on = is_on
        self.mode = mode
        self.fan_speed = fan_speed

    def __repr__(self) -> str:
        """Return representation of the device status."""
        return (
            f"<Status device_id='{self.device_id}', name='{self.name}', model='{self.model}', "
            + f"firmware_version='{self.firmware_version}', "
            + f"wifi_firmware_version='{self.wifi_firmware_version}', "
            + f"is_on={self.is_on}, mode={self.mode}, fan_speed={self.fan_speed}>"
        )


class CannotConnect(Exception):
    """
    Error to indicate we cannot connect.

    Currently only used by the connection test.
    """


class _Command:
    def __init__(self, data: dict[str, Union[str, int, bool]], result: Future[Union[bool, None]]):
        self.data = data
        self.result = result


class PersistentClient:
    """
    PersistentClient attempts to provide reliable communication with the Air Purifier.

    It does so by more or less aggressively timing out requests and retrying them.

    It also provides an interface with Python data types, abstracting from the purifier-provided
    JSON structures.

    Note: Do NOT use multiple clients to connect from one machine to a single Air Purifier.
          Only one of the clients seems receive responses in this case.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, host: str, port: int) -> None:
        """Create a client. Does not connect yet."""
        self._loop = loop
        self._host = host
        self._port = port
        self._background_task: asyncio.Task[None] | None = None
        self._commmand_queue: asyncio.Queue[_Command] = asyncio.Queue()
        # dict key is a unique id that can later be used to remove the observer.
        self._status_callbacks: dict[int, Callable[[Status | None], None]] = {}
        self._last_status_at: datetime = datetime.now(timezone.utc)
        # The purifier sends a status update whenever something changes, which most commonly is the
        # measured pm25 value. When turned on, this usually happens every few seconds to every few
        # 10s of seconds, depending on how the amount of particles in the air changes.
        # When turned off, the updates usually only happen every 3 minutes, sometimes a bit
        # more rarely, though, so let's go with 10 minutes.
        self._status_timeout = timedelta(minutes=10)
        self._shutdown: asyncio.Future[None] = asyncio.Future()

    @staticmethod
    async def test_connection(host: str, port: int) -> dict[str, str]:
        """
        Test if we can connect to the purifier by requesting it's status.

        Returns the device's name, ID, and model.
        """

        try:
            client = await asyncio.wait_for(CoAPClient.create(host=host, port=port), timeout=5.0)
            try:
                info = await asyncio.wait_for(client.info(), timeout=15.0)
            finally:
                await client.shutdown()
        except Exception as ex:
            _LOGGER.error("Philips Air Purifier: Failed to connect: %s", repr(ex))
            raise CannotConnect() from ex

        if "device_id" in info and "name" in info:
            return {
                "name": info["name"],
                "device_id": info["device_id"],
                "model": info["modelid"],
            }

        raise CannotConnect()

    def start(self) -> None:
        """
        Start the client, always trying to keep a connection open.

        If the client has been started before, nothing happens.
        """

        if self._background_task is not None:
            return

        self._background_task = self._loop.create_task(self._connection_loop())

    def stop(self) -> None:
        """Stop the client and close all open connections."""
        # Use cancel, so nothing breaks in case this is called multiple times.
        self._shutdown.cancel()

    async def _connection_loop(self) -> None:
        while True:
            _LOGGER.debug("connecting")

            # Notify all observers that the device is currently unavailable
            for callback in self._status_callbacks.values():
                callback(None)

            try:
                client_create = CoAPClient.create(host=self._host, port=self._port)
                client = await asyncio.wait_for(client_create, timeout=10.0)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception while connecting, reattempting in 10s")
                await asyncio.sleep(10.0)
                continue

            _LOGGER.debug("connected, starting status observations and command loop")

            # Reset status timeout
            self._last_status_at = datetime.now(timezone.utc)

            observe_task = self._loop.create_task(self._observe_status(client))
            status_watchdog = self._loop.create_task(self._status_watchdog())
            keepalive_loop = self._loop.create_task(self._keepalive_loop(client))
            command_loop = self._loop.create_task(self._command_loop(client))
            await asyncio.wait(
                [command_loop, status_watchdog, keepalive_loop, self._shutdown],
                return_when=FIRST_COMPLETED,
            )

            # Connection is broken or shutdown was requested, so abort all tasks
            # (we only wait for the first to complete).
            observe_task.cancel()
            status_watchdog.cancel()
            keepalive_loop.cancel()
            command_loop.cancel()

            try:
                await client.shutdown()
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Client shutdown failed")

            if self._shutdown.cancelled():
                _LOGGER.debug("shutdown requested, stopping connection loop")
                return

    async def _observe_status(self, client: CoAPClient) -> None:
        async for json_status in client.observe_status():
            _LOGGER.debug("observed status: %s", repr(json_status))
            try:
                status = Status(
                    device_id=json_status["DeviceId"],
                    name=json_status["name"],
                    model=json_status["modelid"],
                    firmware_version=json_status["swversion"],
                    wifi_firmware_version=json_status["WifiVersion"],
                    is_on=(json_status["pwr"] == "1"),
                    mode=Mode(json_status["mode"]),
                    fan_speed=FanSpeed(json_status["om"]),
                )
            except KeyError:
                _LOGGER.exception("Failed to read status JSON")
                continue

            _LOGGER.debug("converted status: %s", repr(status))

            self._last_status_at = datetime.now(timezone.utc)
            for callback in self._status_callbacks.values():
                callback(status)

    async def _status_watchdog(self) -> None:
        while True:
            duration_until_timeout = (self._last_status_at + self._status_timeout) - datetime.now(
                timezone.utc
            )

            if duration_until_timeout <= timedelta(0):
                _LOGGER.info("Status not received (timed out), reconnecting")
                # Timed out, return to reconnect.
                return

            await asyncio.sleep(duration_until_timeout.total_seconds())

    # TODO Explain
    async def _keepalive_loop(self, client: CoAPClient) -> None:
        """
        _keepalive_loop sends a device info request about every 60 seconds to
        make sure a potential NAT between the client and the device doesn't
        drop the NAT mapping for the UDP stream.

        It's also useful for detecting connection issues and marking the device
        as unavailable faster than waiting for the status timeout, which needs
        to be quite long.
        """
        while True:
            try:
                await asyncio.wait_for(client.info(), timeout=10.0)
            except Exception:
                _LOGGER.exception("keepalive info failed")
                return

            _LOGGER.debug("Keepalive info successful")

            await asyncio.sleep(60.0)

    async def _command_loop(self, client: CoAPClient) -> None:
        # Empty command queue, so piled up commands don't all time out.
        while not self._commmand_queue.empty():
            cmd = await self._commmand_queue.get()
            cmd.result.set_result(None)

        while True:
            cmd = await self._commmand_queue.get()
            try:
                _LOGGER.debug(
                    "client set_control_values data: %s",
                    repr(cmd.data),
                )
                success = await client.set_control_values(cmd.data)
                cmd.result.set_result(success)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Command failed, reconnecting")
                cmd.result.set_result(None)

                # Command failed, so the connection is probably broken.
                # Return to the connection loop for reconnecting.
                return

    async def _run_command(
        self,
        data: dict[str, Union[str, int, bool]],
    ) -> bool | None:

        result_future: Future[bool | None] = self._loop.create_future()
        cmd = _Command(data=data, result=result_future)
        await self._commmand_queue.put(cmd)
        return await result_future

    async def turn_on(self) -> None:
        """Turn the purifier on."""
        success = await self._run_command(data={"pwr": "1"})
        if not success:
            _LOGGER.error("Failed to turn on")

    async def turn_off(self) -> None:
        """Turn the purifier off."""
        success = await self._run_command(data={"pwr": "0"})
        if not success:
            _LOGGER.error("Failed to turn off")

    async def set_preset_mode(self, mode: Mode) -> None:
        """Activate a preset mode on the purifier."""
        success = await self._run_command(data={"mode": mode.value})
        if not success:
            _LOGGER.error("Failed to set preset_mode %s", mode)

    async def set_manual_speed(self, speed: FanSpeed) -> None:
        """Set the fan to a constant speed."""
        success = await self._run_command(data={"om": speed.value})
        if not success:
            _LOGGER.error("Failed to set manual speed %s", speed)

    def observe_status(self, id_: int, callback: Callable[[Status | None], None]) -> None:
        """
        Register the given callable to be called when the client reveives a status update from the
        purifier.

        The client passes None as status to the callback if the device is unavailable.
        """
        _LOGGER.debug("observing status")
        self._status_callbacks[id_] = callback

    def stop_observing_status(self, id_: int) -> None:
        """Unregister the callable previously registered with the given id from status updates."""
        _LOGGER.debug("stopped observing status")
        del self._status_callbacks[id_]
