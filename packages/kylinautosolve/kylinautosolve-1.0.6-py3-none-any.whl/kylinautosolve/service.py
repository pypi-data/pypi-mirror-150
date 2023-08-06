# pylint: disable=unused-argument
import asyncio

from .client import KylinAutosolveClient, KylinAutosolveError, CreateTaskRequest
from .client import KylinAutosolveProto


class KylinAutosolveService:
    """
    A light weight wrapper for the ``kylinautosolve.KylineAutosolveClient``

    You may use this class as a base for your own client and implement more complex logic, such as
    request cancellation.
    """
    def __init__(self, client_key: str) -> None:
        self.client_key: str = client_key
        self.client: KylinAutosolveClient = KylinAutosolveClient()
        self.unhandled_result: dict = {}
        self.task_futures: dict = {}

        self._register_handler(self.client)

    def start(self, access_token: str) -> None:
        """
        Start the client.
        """
        self.client.access_token = access_token
        self.client.client_key = self.client_key
        self.client.start()

    async def when_ready(self) -> None:
        """
        Wait until the client is ready.
        """
        return await self.client.when_ready()

    def stop(self) -> None:
        """
        Stop the client.
        """
        self.client.stop()

    async def solve(self, request: CreateTaskRequest) -> KylinAutosolveProto.TaskResultNotification:
        """
        Create a task and wait for the result.
        """
        await self.when_ready()

        create_task_message = self.client.make_create_task_message(request)
        create_task_response = await self.client.invoke(create_task_message)
        task_info = create_task_response.create_task
        if not task_info or task_info.error_id != 0 or not task_info.task_id:
            raise KylinAutosolveError('could not create task')
        task_id = task_info.task_id

        if task_id in self.unhandled_result:
            result = self.unhandled_result.pop(task_id)
            return result

        future = asyncio.Future()
        self.task_futures[task_id] = future
        return await future

    def _register_handler(self, client: KylinAutosolveClient) -> None:
        client.on('notification:task_result', self._on_task_result)

    def _on_task_result(self, evt, *args, **kwargs) -> None:
        notification = evt.notification
        task_result = notification.task_result
        evt.handled += 1

        if task_result.task_id in self.task_futures:
            future = self.task_futures[task_result.task_id]
            del self.task_futures[task_result.task_id]
            future.set_result(task_result)
        else:
            self.unhandled_result[task_result.task_id] = task_result
