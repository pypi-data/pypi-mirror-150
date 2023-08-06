# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument
# pylint: disable=bare-except
# pylint: disable=line-too-long
# pylint: disable=broad-except
"""
This module contains the websocket based clinet for Kylin Autosolve
"""
from __future__ import annotations

import asyncio
import traceback
import json
from pyee import AsyncIOEventEmitter


from .rpc.transport import KylinRpcTransport, State
from .pb import kylinautosolve_pb2 as KylinAutosolveProto

DEFAULT_AUTOSOLVE_ENDPOINT = "wss://autosolve-ws.kylinbot.io/ws"
RECONNECT_INTERNVALS = [1000, 2000, 4000, 8000, 16000]
HEARTBEAT_INTERVAL = 10


class KylinAutosolveError(Exception):
    """
    The base class for our excepts
    """


class AlreadyStartedError(KylinAutosolveError):
    """
    Raised when the client is already started
    """


class NotStartedError(KylinAutosolveError):
    """
    Raised when the client is not started
    """


class NotConnectedError(KylinAutosolveError):
    """
    Raised when the connection is broken
    """


class StoppedError(KylinAutosolveError):
    """
    Raised when the client is stopped already
    """


class RequestAbortedError(KylinAutosolveError):
    """
    Raised when the client is stopped for pending requests
    """


class InvalidCredentialsError(KylinAutosolveError):
    """
    Raised when the credentials are invalid
    """


class RemoteError(KylinAutosolveError):
    """
    Raised when the server returns an error
    """
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class NotificationEvent:
    """
    An event that is emitted when a notification is received
    """

    def __init__(self, sender: KylinAutosolveClient, msg: KylinAutosolveProto.Message, notification: KylinAutosolveProto.Notification) -> None:
        self.sender = sender
        self.handled = 0
        self.msg = msg
        self.notification = notification


class CreateTaskRequest:
    """
    A request to create a task
    """
    def __init__(self, challenge_type: str, url: str, timeout: int = 0, options: str | dict = None) -> None:
        if isinstance(options, dict):
            options = json.dumps(options)
        self.challenge_type: str = challenge_type
        self.url: str = url
        self.timeout: int = timeout
        self.options: str = options


class GetTaskResultRequest:
    """
    A request to get the result of a task
    """
    def __init__(self, task_id: str) -> None:
        self.task_id: str = task_id


class CancelTaskRequest:
    """
    A request to cancel a task
    """

    def __init__(self, challenge_type: str = '', task_id: str = '') -> None:
        self.challenge_type: str = challenge_type
        self.task_id: str = task_id


class KylinAutosolveClient(AsyncIOEventEmitter):
    """
    A kylin autosolve client using the websocket based protocol
    """

    def __init__(self) -> None:
        super().__init__()
        self.logged_in: bool = False
        self.endpoint: str = DEFAULT_AUTOSOLVE_ENDPOINT
        self.access_token: str = ''
        self.client_key: str = ''
        self.started: bool = False
        self._next_request_id: int = 1
        self.requests: dict = {}
        self.login_error: bool = False
        self.started: bool = False
        self.retry_count: int = 0
        self.heartbeat_check_count: int = 0
        self.heartbeat_check_timeout_count: int = 8
        self.transport: KylinRpcTransport = KylinRpcTransport()
        self.reconnect_task: asyncio.Task = None
        self.heartbeat_check_task: asyncio.Task = None

        self._register_event_handlers()

    async def when_ready(self) -> None:
        """
        Wait for this client to be ready
        """
        if not self.started:
            raise NotStartedError("start this client first")
        if self.logged_in:
            return

        futures = asyncio.Future()

        class Handlers:
            """
            Internal
            """
            def __init__(self) -> None:
                self.stop = False
                self.login_error = False
                self.login = False

        handlers = Handlers()
        handlers.stop = False
        handlers.login = False
        handlers.login_error = False

        def on_login(*args, **kwargs):
            handlers.login = True
            futures.set_result(True)

        def on_login_error(ex, *args, **kwargs):
            handlers.login_error = True
            futures.set_exception(ex or KylinAutosolveError('unknown error'))

        def on_stop(*args, **kwargs):
            handlers.stop = True
            futures.set_exception(StoppedError('this client is stopped'))

        self.once('on_stop', on_stop)
        self.once('login', on_login)
        self.once('login-error', on_login_error)
        try:
            await futures
        finally:
            if not handlers.stop:
                self.remove_listener('on_stop', on_stop)
            if not handlers.login:
                self.remove_listener('login', on_login)
            if not handlers.login_error:
                self.remove_listener('login-error', on_login_error)

    def start(self) -> None:
        """
        Start this client
        """
        if self.started:
            raise AlreadyStartedError(
                "stop this client before starting it again")
        self.started = True
        self._connect()

    def stop(self) -> None:
        """
        Stop the client

        All pending requests will be aborted.
        """
        self._stop()
        try:
            self.emit('stop')
        except:
            traceback.print_exc()

    def _stop(self) -> None:
        if not self.started:
            return
        self.started = False
        self.logged_in = False
        self.retry_count = 0
        self.__abort_requests()
        self.transport.disconnect()

        if self.reconnect_task:
            if not self.reconnect_task.cancelled():
                self.reconnect_task.cancel()
        self.reconnect_task = None

    async def invoke(self, msg: KylinAutosolveProto.Message) -> KylinAutosolveProto.Response:
        """
        invoke a remote call
        """
        if not self.started:
            raise NotStartedError('start this client first')
        if self.transport.state != State.CONNECTED:
            raise NotConnectedError('not connected')

        if not msg.request_id:
            msg.request_id = self.next_request_id()
        request_id = msg.request_id

        future = asyncio.Future()
        self.requests[request_id] = future
        await self.transport.send(msg.SerializeToString())
        try:
            result = await future
        finally:
            if request_id in self.requests:
                del self.requests[request_id]
        return result

    def make_login_message(self) -> KylinAutosolveProto.Message:
        """
        Make a login request
        """
        msg = KylinAutosolveProto.Message()
        msg.message_type = KylinAutosolveProto.REQUEST
        msg.request_id = self.next_request_id()

        payload = msg.request.login
        payload.access_token = self.access_token
        payload.client_key = self.client_key
        return msg

    def make_create_task_message(self, create_task_request: CreateTaskRequest) -> KylinAutosolveProto.Message:
        """
        Make a message to create a task
        """
        msg = KylinAutosolveProto.Message()
        msg.message_type = KylinAutosolveProto.REQUEST
        msg.request_id = self.next_request_id()

        payload = msg.request.create_task
        payload.challenge_type = create_task_request.challenge_type
        payload.url = create_task_request.url
        if create_task_request.timeout:
            payload.time_out = create_task_request.timeout
        if create_task_request.options:
            payload.options = create_task_request.options
        else:
            payload.options = '{}'
        return msg

    def make_get_task_result_message(self, req: GetTaskResultRequest) -> KylinAutosolveProto.Message:
        """
        Make a message to get the result of a task
        """
        msg = KylinAutosolveProto.Message()
        msg.message_type = KylinAutosolveProto.REQUEST
        msg.request_id = self.next_request_id()

        payload = msg.request.get_task_result
        payload.task_id = req.task_id
        return msg

    def make_cancel_task_message(self, req: CancelTaskRequest = None) -> KylinAutosolveProto.Message:
        """
        Make a message to cancel a task, tasks with given type or all tasks
        """
        msg = KylinAutosolveProto.Message()
        msg.message_type = KylinAutosolveProto.REQUEST
        msg.request_id = self.next_request_id()

        payload = msg.request.cancel_task
        if req and req.challenge_type:
            payload.challenge_type = req.challenge_type
        if req and req.task_id:
            payload.task_id = req.task_id
        if not req or (not req.challenge_type and not req.task_id):
            payload.task_id = ''
        return msg

    def next_request_id(self) -> int:
        """
        Returns the next request id
        """
        result = self._next_request_id
        self._next_request_id += 1
        return result

    def _connect(self) -> None:
        self.transport.disconnect()
        self.transport.connect(self.endpoint)

    def _restart(self) -> None:
        self._stop()
        self.start()

    def _register_event_handlers(self) -> None:
        self.transport.on('connected', self._on_connected)
        self.transport.on('disconnected', self._on_disconnected)
        self.transport.on('connect-error', self._on_connect_error)
        self.transport.on('message', self._on_message)

    def _on_connected(self, *args, **kwargs):
        if self.started:
            self.__start_heartbeat()
            asyncio.create_task(self._login())

    def _on_disconnected(self, *args, **kwargs):
        if self.started:
            self.logged_in = False
            self.__abort_requests()
            self.__stop_heartbeat()

            try:
                self.emit('disconnected')
            except:
                traceback.print_exc()

            self._sleep_and_reconnect()

    def _on_connect_error(self, e, *args, **kwargs):
        if self.started:
            self.__abort_requests()
            self.__stop_heartbeat()

            try:
                self.emit('connect-error', e)
            except:
                traceback.print_exc()

            self._sleep_and_reconnect()

    async def _on_message(self, data: bytes, *args, **kwargs):
        msg = KylinAutosolveProto.Message()
        msg.ParseFromString(data)
        if msg.HasField('request'):
            await self._handle_request(msg)
        elif msg.HasField('notification'):
            await self._handle_notification(msg)
        elif msg.HasField('response'):
            await self._handle_response(msg)

    async def _handle_request(self, msg: KylinAutosolveProto.Message):
        request = msg.request
        if request.WhichOneof('payload') == 'ping':
            self.heartbeat_check_count = 0
            await self._send_ping_response(msg)
        else:
            await self._send_error(
                msg, KylinAutosolveProto.ErrorCode.INVALID_REQUEST, 'unsupported request')

    async def _handle_response(self, msg: KylinAutosolveProto.Message):
        response = msg.response
        request_id = msg.request_id

        futures: asyncio.Future = self.requests.get(request_id, None)
        del self.requests[request_id]

        if response.HasField("error"):
            error = response.error
            futures.set_exception(RemoteError(error.code, error.message))
        else:
            futures.set_result(response)

    async def _handle_notification(self, msg: KylinAutosolveProto.Message):
        notification = msg.notification
        evt = NotificationEvent(self, msg, notification)

        payload_type = notification.WhichOneof('payload')
        try:
            self.emit('notification:' + payload_type, evt)
        except:
            traceback.print_exc()
        if not evt.handled:
            try:
                self.emit('notification', evt)
            except:
                traceback.print_exc()

    def _sleep_and_reconnect(self):
        self.retry_count += 1

        sleep_time = RECONNECT_INTERNVALS[self.retry_count % len(
            RECONNECT_INTERNVALS)] / 1000.0
        reconnect_task = None

        async def reconnect():
            await asyncio.sleep(sleep_time)
            if self.reconnect_task == reconnect_task and self.started and self.transport.state != State.CONNECTED:
                self._connect()
        reconnect_task = asyncio.create_task(reconnect())
        self.reconnect_task = reconnect_task

    def __abort_requests(self) -> None:
        request_ids = list(self.requests.keys())
        for request_id in request_ids:
            futures: asyncio.Future = self.requests.get(request_id, None)
            del self.requests[request_id]
            futures.set_exception(RequestAbortedError('request aborted'))
        self.requests = {}

    async def ___start_heartbeat(self) -> None:
        while self.started:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            self.heartbeat_check_count += 1
            if self.heartbeat_check_count > self.heartbeat_check_timeout_count:
                self._restart()

    def __start_heartbeat(self) -> None:
        self.heartbeat_check_task = asyncio.create_task(
            self.___start_heartbeat())

    def __stop_heartbeat(self) -> None:
        if self.heartbeat_check_task:
            self.heartbeat_check_task.cancel()
        self.heartbeat_check_task = None

    async def _login(self) -> None:
        try:
            response: KylinAutosolveProto.Response = await self.invoke(self.make_login_message())

            login_response: KylinAutosolveProto.LoginResponse = response.login
            if login_response.success:
                self.logged_in = True
                self.login_error = False
                try:
                    self.emit('login')
                except:
                    traceback.print_exc()
            else:
                self.logged_in = False
                self.login_error = True
                try:
                    self.emit('login-error',
                              InvalidCredentialsError('invalid credentials'))
                except:
                    traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
            self.login_error = True
            try:
                self.emit('login-error', e)
            except:
                traceback.print_exc()

    async def _send_ping_response(self, msg) -> None:
        response_msg = KylinAutosolveProto.Message()
        response_msg.message_type = KylinAutosolveProto.RESPONSE
        response_msg.request_id = msg.request_id
        response_msg.response.ping.time = msg.request.ping.time
        await self.transport.send(response_msg.SerializeToString())

    async def _send_error(self, msg: KylinAutosolveProto.Message, code: int, error_message: str = ""):
        msg = KylinAutosolveProto.Message()
        msg.request_id = msg.request_id
        error = msg.response.error
        error.code = code
        error.message = error_message
        await self.transport.send(msg.SerializeToString())
