from __future__ import annotations

import json
import logging
import os
from typing import Any, AsyncIterator, Type, TypeVar, Union

from aiocoap import GET, NON, POST, Context, Message

from phipsair.coap import aiocoap_monkeypatch  # noqa: F401
from phipsair.coap.encryption import EncryptionContext

logger = logging.getLogger(__name__)

ClientT = TypeVar("ClientT", bound="Client")


class Client:
    INFO_PATH = "/sys/dev/info"
    STATUS_PATH = "/sys/dev/status"
    CONTROL_PATH = "/sys/dev/control"
    SYNC_PATH = "/sys/dev/sync"

    def __init__(self, host: str, port: int = 5683) -> None:
        self.host = host
        self.port = port
        self._client_context = None
        self._encryption_context: EncryptionContext | None = None

    async def _init(self) -> None:
        self._client_context = await Context.create_client_context()
        self._encryption_context = EncryptionContext()
        await self._sync()

    @classmethod
    async def create(cls: Type[ClientT], host: str, port: int = 5683) -> ClientT:
        obj = cls(host, port)
        await obj._init()
        return obj

    async def shutdown(self) -> None:
        if self._client_context:
            await self._client_context.shutdown()

    async def _sync(self) -> None:
        assert self._client_context is not None

        logger.debug("syncing")
        sync_request = os.urandom(4).hex().upper()
        request = Message(
            code=POST,
            mtype=NON,
            uri=f"coap://{self.host}:{self.port}{self.SYNC_PATH}",
            payload=sync_request.encode(),
        )
        response = await self._client_context.request(request).response
        client_key = response.payload.decode()
        logger.debug("synced: %s", client_key)
        self._encryption_context.set_client_key(client_key)

    async def info(self) -> dict[str, str]:
        assert self._client_context is not None

        logger.debug("calling info")
        request = Message(
            code=GET,
            mtype=NON,
            uri=f"coap://{self.host}:{self.port}{self.INFO_PATH}",
        )
        response = await self._client_context.request(request).response
        payload = response.payload.decode()
        logger.debug("info: %s", payload)
        return json.loads(payload)

    async def get_status(self) -> dict[str, Any]:
        assert self._client_context is not None
        assert self._encryption_context is not None

        logger.debug("retrieving status")
        request = Message(
            code=GET,
            mtype=NON,
            uri=f"coap://{self.host}:{self.port}{self.STATUS_PATH}",
        )
        request.opt.observe = 0
        response = await self._client_context.request(request).response
        payload_encrypted = response.payload.decode()
        payload = self._encryption_context.decrypt(payload_encrypted)
        logger.debug("status: %s", payload)
        state_reported = json.loads(payload)
        return state_reported["state"]["reported"]

    async def observe_status(self) -> AsyncIterator[dict[str, Any]]:
        assert self._client_context is not None

        def decrypt_status(response):
            assert self._encryption_context is not None

            payload_encrypted = response.payload.decode()
            payload = self._encryption_context.decrypt(payload_encrypted)
            logger.debug("observation status: %s", payload)
            status = json.loads(payload)
            return status["state"]["reported"]

        logger.debug("observing status")
        request = Message(
            code=GET,
            mtype=NON,
            uri=f"coap://{self.host}:{self.port}{self.STATUS_PATH}",
        )
        request.opt.observe = 0
        requester = self._client_context.request(request)
        response = await requester.response
        yield decrypt_status(response)
        async for response in requester.observation:
            yield decrypt_status(response)

    async def set_control_value(
        self, key: str, value: Union[str, int, bool], retry_count: int = 5, resync: bool = True
    ) -> bool:
        return await self.set_control_values(
            data={key: value}, retry_count=retry_count, resync=resync
        )

    async def set_control_values(
        self, data: dict[str, Union[str, int, bool]], retry_count: int = 5, resync: bool = True
    ) -> bool:
        assert self._client_context is not None
        assert self._encryption_context is not None

        state_desired: dict[str, Any] = {
            "state": {
                "desired": {
                    "CommandType": "app",
                    "DeviceId": "",
                    "EnduserId": "",
                    **data,
                }
            }
        }
        payload = json.dumps(state_desired)
        logger.debug("REQUEST: %s", payload)
        payload_encrypted = self._encryption_context.encrypt(payload)
        request = Message(
            code=POST,
            mtype=NON,
            uri=f"coap://{self.host}:{self.port}{self.CONTROL_PATH}",
            payload=payload_encrypted.encode(),
        )
        response = await self._client_context.request(request).response
        logger.debug("RESPONSE: %s", response.payload)
        result = json.loads(response.payload)
        if result.get("status") == "success":
            return True
        else:
            if resync:
                logger.debug("set_control_value failed. resyncing...")
                await self._sync()
            if retry_count > 0:
                logger.debug("set_control_value failed. retrying...")
                return await self.set_control_values(data, retry_count - 1, resync)
            logger.error("set_control_value failed: %s", data)
            return False
