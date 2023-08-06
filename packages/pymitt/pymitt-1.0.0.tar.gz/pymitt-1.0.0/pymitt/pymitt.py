"""pymitt - a simple wrapper for the Keymitt api"""

import asyncio
import aiohttp

from abc import ABC
from string import Template


class KeymittBase(ABC):

    API_BASE = "https://o1.keymitt.com/km/do"

    def __init__(self,
                 device_id: str,
                 token: str,
                 loop: asyncio.AbstractEventLoop or None = None,
                 session: aiohttp.client.ClientSession or None = None):
        self._device_id = device_id
        self._token = token
        self._api_template = Template(f"{self.API_BASE}/$verb?_id={self._device_id}&_tk={self._token}")
        self._session = aiohttp.ClientSession(loop=loop or asyncio.get_event_loop()) if not session else session

    async def _call_api_for_verb(self, verb: str) -> bool:
        uri = self._build_uri_for_verb(verb)

        async with self._session.get(uri) as response:
            return True if response.status == 200 else False

    def _build_uri_for_verb(self, verb: str) -> str:
        return self._api_template.substitute({"verb": verb})


class KeymittLock(KeymittBase):

    async def lock(self) -> bool:
        return await self._call_api_for_verb("lock")

    async def unlock(self) -> bool:
        return await self._call_api_for_verb("unlock")

class KeymittPush(KeymittBase):

    async def press(self) -> bool:
        return await self._call_api_for_verb("press")

    async def push(self) -> bool:
        return await self._call_api_for_verb("push")

    async def release(self) -> bool:
        return await self._call_api_for_verb("release")
