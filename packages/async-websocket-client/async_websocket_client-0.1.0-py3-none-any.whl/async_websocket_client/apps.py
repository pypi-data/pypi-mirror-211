from __future__ import annotations

import asyncio
import logging
from typing import Any, Coroutine

import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError

from async_websocket_client.dispatchers import BaseDispatcher

# from sdk.client import BaseDispatcher


logger = logging.getLogger('async_websocket_client')


class AsyncWebSocketApp(object):
    url: str
    dispatcher: BaseDispatcher
    ws: WebSocketClientProtocol

    is_running: bool

    def __init__(self, url: str, dispatcher: BaseDispatcher):
        self.url = url
        self.dispatcher = dispatcher
        self.dispatcher.set_app(self)

        self.is_running = False

    async def connect(self):
        await self.dispatcher.before_connect()
        self.ws = await websockets.connect(self.url)
        await self.dispatcher.set_websocket(self.ws)
        await self.dispatcher.on_connect()

        self.is_running = True

    async def disconnect(self):
        self.is_running = False

        await self.dispatcher.before_disconnect()
        await self.ws.close()
        await self.dispatcher.on_disconnect()

    async def send(self, message: str) -> Any:
        return await self.ws.send(message)

    async def ws_recv_message(self) -> str | None:
        try:
            return await asyncio.wait_for(self.ws.recv(), 1)

        except asyncio.TimeoutError:
            return None

    async def ws_recv_loop(self):
        while self.is_running:
            message = await self.ws.recv()
            if message is None:
                continue

            await self.dispatcher.on_message(message)

    async def run(self):
        await self.connect()

        try:
            await self.ws_recv_loop()

        except asyncio.exceptions.CancelledError as ex:
            logger.error([type(ex), ex])

        except ConnectionClosedError as e:
            logger.error(f'Connection closed with error: {e}')

        await self.disconnect()

    def asyncio_run(self):
        try:
            asyncio.run(self.run())

        except KeyboardInterrupt:
            logger.info('Correct exit')
