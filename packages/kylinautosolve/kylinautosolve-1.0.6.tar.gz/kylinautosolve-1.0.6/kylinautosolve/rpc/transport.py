# pylint: disable=bare-except
# pylint: disable=broad-except
"""
This module contains the websocket based transport for kylin rpc
"""
import asyncio
import enum
import traceback
import websockets
from pyee import AsyncIOEventEmitter


class State(enum.Enum):
    """
    The state of the websocket connection.
    """
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3


class KylinRpcTransport(AsyncIOEventEmitter):
    """
    A websocket based transport for kylin rpc
    """
    def __init__(self) -> None:
        super().__init__()
        self._connect: websockets.client.Connect = None
        self._ws: websockets.WebSocketClientProtocol = None
        self._run_task: asyncio.Task = None

    @property
    def ws(self):
        return self._ws

    @property
    def state(self):
        if self.ws:
            return State.CONNECTED
        if self._connect:
            return State.CONNECTING
        return State.DISCONNECTED

    async def _emit_message(self, ws, msg):
        try:
            if self._ws == ws:
                self.emit('message', msg)
        except:
            traceback.print_exc()

    async def run(self):
        try:
            async with self._connect as ws:
                self._connect = None
                self._ws = ws
                try:
                    self.emit('connected')
                except:
                    traceback.print_exc()
                while self._ws == ws:
                    msg = await ws.recv()
                    asyncio.create_task(self._emit_message(ws, msg))
        except Exception as e:
            traceback.print_exc()
            if self._ws:
                self.disconnect()
                try:
                    self.emit('disconnected', e)
                except:
                    traceback.print_exc()
            else:
                try:
                    self.emit('connect-error', e)
                except:
                    traceback.print_exc()

    def connect(self, url):
        """
        connect to the server
        """
        self._connect = websockets.connect(url)
        self._run_task = asyncio.create_task(self.run())

    def disconnect(self):
        """
        disconnect from the server
        """
        if self._run_task and not self._run_task.done() and not self._run_task.cancelled():
            self._run_task.cancel()
        self._run_task = None
        if self._ws and self._ws.state == websockets.protocol.State.OPEN:
            asyncio.create_task(self._ws.close())
        self._connect = None
        self._ws = None

    async def send(self, message):
        """
        send a message to the server
        """
        return await self._ws.send(message)
