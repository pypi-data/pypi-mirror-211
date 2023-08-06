# -*- coding: utf-8 -*-
from asyncio import AbstractEventLoop, get_event_loop

import uuid
import warnings
from datetime import datetime
from typing import Tuple, Mapping, Any, Callable, Union, Iterable, Type

import pytz
from pydantic import validate_model

from .serializers.base import BaseTaskSerializer
from .serializers.betterproto import BetterprotoSerializer
from .task import Task, TaskMetadata, TaskDecodeError
from ..component import Component


class PatchworkPublisher(Component):
    """
    Common code for sync and async publishers
    """

    class Config(Component.Config):
        """
        Settings schema for each Patchwork Client.
        :cvar max_message_size:     Maximum allowed message size (on the wire) in bytes
        """
        max_message_size: int = 1024*1024       # 1MB
        serializer: Type[BaseTaskSerializer] = BetterprotoSerializer

    settings: Config
    asynchronous: bool
    routing: list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routing = []
        self.task_serializer = self.settings.serializer()

    def __repr__(self):
        return super().__repr__().replace('Component', 'Publisher')

    def add_router(self, router: Callable[[Task], Union[str, None]]):
        """
        Add a task router for the publisher. Routers will be executed in the reverse order of adding
        (the most newly added - firstly executed)
        :param router: callable which for given task returns a name of queue for it or None if this router
        does not support this task
        :return:
        """
        self.routing.insert(0, router)

    def remove_router(self, router: Callable[[Task], Union[str, None]]):
        """
        Removes previously added router
        :param router:
        :return:
        """
        self.routing.remove(router)

    def _serialize_task(self, task: Task) -> bytes:
        """
        Take task and returns serialized task payload as bytes.
        :param task:    Task instance
        :return:    Serialized task
        """
        *_, errors = validate_model(Task, task.__dict__)
        if errors:
            raise errors
        return self.task_serializer.encode(task)

    def _prepare_task(self, task: Task) -> bytes:
        """
        Prepares task to be send. Makes validation tests on the task and returns serialized payload.
        Internally this method calls _serialize_task()
        :param task:
        :raise ValueError: if task validation fails
        :return: payload of serialized task if validation pass
        """
        if not task.uuid:
            task.uuid = str(uuid.uuid4())
        task.meta.scheduled = datetime.now(pytz.UTC)

        if task.meta.expires and task.meta.expires < task.meta.scheduled:
            raise ValueError('unable to send task which is already expired')

        if not task.meta.queue_name:
            for router in self.routing:
                queue_name = router(task)
                if queue_name is not None:
                    break

        payload = self._serialize_task(task)
        if len(payload) > self.settings.max_message_size:
            raise ValueError('message is too big')

        return payload

    def _build_task(self, payload: Any, meta: Union[Mapping, TaskMetadata], cause: Task = None, task_type: str = None):
        if not isinstance(meta, TaskMetadata):
            meta = dict(meta)
            metadata = TaskMetadata()

            if 'not_before' in meta:
                metadata.not_before = meta.pop('not_before')
            if 'expires' in meta:
                metadata.expires = meta.pop('expires')
            if 'max_retries' in meta:
                metadata.max_retries = meta.pop('max_retries')
            if 'queue_name' in meta:
                metadata.queue_name = meta.pop('queue_name')

            if meta:
                metadata.extra = dict(meta)
        else:
            metadata = meta

        task = Task(
            uuid=uuid.uuid4(),
            meta=metadata,
            task_type=task_type or payload.__class__.__name__,
            payload=payload
        )

        if cause is not None:
            task.correlation_id = cause.correlation_id or str(cause.uuid)

        return task

    def __del__(self):
        if self.is_running:
            warnings.warn(f"Destroying unstopped publisher may leads to data loss! stop() didn't finished or called")


class PatchworkSubscriber(Component):

    class Config(Component.Config):
        """
        Settings schema for each Patchwork Client.
        """
        serializer: Type[BaseTaskSerializer] = BetterprotoSerializer

    settings: Config
    asynchronous: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_serializer = self.settings.serializer()

    def __repr__(self):
        return super().__repr__().replace('Component', 'Subscriber')

    def _deserialize_task(self, payload: bytes, meta: Mapping) -> Task:
        """
        Deserialize given payload as a Task.
        :param payload:
        :param meta:    Additional data passed by receiver
        :return:        Deserialized task instance
        """
        return self.task_serializer.decode(payload)

    def _process_received_task(self, payload: bytes, meta: Mapping) -> Task:
        """
        Processes received payload and converts into task. Internally this method calls _deserialize_task()
        :param payload:
        :param meta:    additional informaction passed by a receiver
        :return:  deserialized task instance
        """
        try:
            task = self._deserialize_task(payload, meta)
        except Exception as exc:
            handled = self._handle_deserialize_error(payload, meta, exc)
            raise TaskDecodeError(payload, meta, exc, handled) from exc

        task.meta.received = datetime.now(pytz.UTC)
        task.meta.queue_name = meta.get('queue_name', None)
        return task

    def _handle_deserialize_error(self, payload: bytes, meta: Any, exc: Exception) -> bool:
        """
        Called when exception is raised during message deserialization and task initialization.
        This method is responsible of making sure that task won't be lost, however simple resending
        to the queue might be not accurate because if error happens once it probably will happen
        every time.
        :param payload:
        :param meta:
        :param exc:
        :return: True if message has been somehow handled and worker should not take any action. Otherwise
                 return False, so worker may report this issue using own logging mechanism
        """
        return False

    def __del__(self):
        if self.is_running:
            warnings.warn(f"Destroying unstopped subscriber may leads to data loss! stop() didn't finished or called")


class SynchronousPublisher(PatchworkPublisher):
    """
    Synchronous patchwork base client. This is a fallback client for external synchronous code
    without async support.
    """

    is_asynchronous = False

    def send(self, payload: Any, *, timeout: float = None, cause: Task = None, **meta):
        task = self._build_task(payload, meta, cause=cause)
        self.send_task(task, timeout=timeout)
        return task

    def send_task(self, task: Task, *, timeout: float = None):
        """
        Sends given task, if operation fail in given timeout raises TimeoutError.
        :param task:
        :param timeout: send operation timeout, None means no timeout
        :return:
        """
        payload = self._prepare_task(task)
        self._send(payload, task, timeout=timeout)

    def _send(self, payload: bytes, task: Task, *, timeout: float = None):
        """
        Sends given payload
        :param payload: Task payload to send
        :param timeout: Requested send operation timeout, None means no timeout
        :return:
        """
        raise NotImplementedError()


class SynchronousSubscriber(PatchworkSubscriber):

    def get(self, *, timeout: int = None):
        """
        Waits given time for next task and when arrived returns it. If no task came raises EOFError.
        :param timeout:
        :return:
        """
        payload, meta = self._fetch_one(timeout=timeout)
        return self._process_received_task(payload, meta)

    def commit(self, task, *, timeout: int = None):
        """
        Commits given task returned by get() method. If operation fail in given timeout
        raises TimeoutError.
        :param task:
        :param timeout:
        :return:
        """
        raise NotImplementedError()

    def _fetch_one(self, *, timeout=None) -> Tuple[bytes, Mapping]:
        """
        Fetch one incoming message from the queue.
        :param timeout: Waits given time for message, if there is no message in given timeout raises TimeoutError.
                        None means no timeout, `0` means no wait.
        :return: payload of fetched message and additional information which should be passed to task deserializer
        """
        raise NotImplementedError()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.get()
        except EOFError:
            raise StopIteration()

    def subscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError()

    def unsubscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError()

    def subscription(self) -> Iterable[str]:
        raise NotImplementedError()


class AsyncPublisher(PatchworkPublisher):
    """
    Patchwork asynchronous pubslisher
    """

    is_asynchronous = True

    def __init__(self, *, parent=None, loop: AbstractEventLoop = None, **options):
        super().__init__(parent=parent, **options)

        if loop is None:
            loop = get_event_loop()

        self.loop = loop

    async def send(self, payload: Any, *, timeout: float = None, cause: Task = None, task_type: str = None, **meta):
        task = self._build_task(payload, meta, cause=cause, task_type=task_type)
        await self.send_task(task, timeout=timeout)
        return task

    async def send_task(self, task: Task, *, timeout: float = None):
        """
        Sends given task, if operation fail in given timeout raises TimeoutError.
        When this method returns it's considered as task has been delivered successfully and it's guaranteed
        that won't be lost (eg queue backend committed the message)
        :param task:
        :param timeout: send operation timeout, None means no timeout. 0 means immediatelly
        :return:
        """
        payload = self._prepare_task(task)
        await self._send(payload, task, timeout=timeout)

    async def _send(self, payload: bytes, task: Task, *, timeout: float = None):
        """
        Sends given payload

        :param payload: Task payload to send
        :param task: Task instance to send, it should be considered as **immutable**
        :param timeout: Requested send operation timeout, None means no timeout, 0 means immediately
        :return:
        """
        raise NotImplementedError()


class AsyncSubscriber(PatchworkSubscriber):

    is_asynchronous = True

    def __init__(self, *, parent=None, loop: AbstractEventLoop = None, **options):
        super().__init__(parent=parent, **options)

        if loop is None:
            loop = get_event_loop()

        self.loop = loop

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.get()
        except EOFError:
            raise StopAsyncIteration()

    async def subscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError()

    async def unsubscribe(self, queue_name: Iterable[str]):
        raise NotImplementedError()

    def subscription(self) -> Iterable[str]:
        raise NotImplementedError()

    async def get(self, *, timeout: float = None) -> Task:
        """
        Waits given time for next task and when arrived returns it.
        :param timeout:
        :raise TimeoutError: no task came in given timeout
        :return:
        """
        payload, meta = await self._fetch_one(timeout=timeout)
        return self._process_received_task(payload, meta)

    async def commit(self, task: Task, *, timeout: float = None):
        """
        Commits given task returned by get() method.
        Meaning of "commit" depends on queue backend, but should be considered as success of task handling
        (which is not the same as success of task execution). Success of task handling means that task
        has been executed successfully or rescheduled successfully and given task can be safely removed
        from the queue. Whatever happens task won't be lost.

        :param task:
        :raise TimeoutError: commit timeout exceeded
        :param timeout:
        :return:
        """
        raise NotImplementedError()

    async def rollback(self, task: Task, *, timeout: float = None):
        """
        Rollback given task returned by get() method.
        Meaning of "rollback" depends on queue backend, but after this operation exactly the same task should
        be delivered again. Use this with caution as exactly the same is strict, so your code will receive
        the same bytes again and again. Make sure that it doesn't lead to infinite loop.

        For retries, it's recommended to store some retries counter in task meta, send retry task explicitly
        with bumped counter and commit the failed one.
        :param task:
        :param timeout:
        :return:
        """
        raise NotImplementedError()

    async def _fetch_one(self, *, timeout: float = None) -> Tuple[bytes, Mapping]:
        """
        Fetch one incoming message from the queue.
        :param timeout: Waits given time for message, if there is no message in given timeout raises TimeoutError.
                        None means no timeout, `0` means no wait.
        :return: payload of fetched message and additional information which should be passed to task deserializer
        """
        raise NotImplementedError()
