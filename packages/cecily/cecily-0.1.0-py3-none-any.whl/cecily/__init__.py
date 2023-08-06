import concurrent.futures
import logging
import multiprocessing
import multiprocessing.connection as mc
import os
import shutil
import tempfile
import threading
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from enum import Enum
from multiprocessing.managers import BaseManager
from pathlib import Path
from typing import Any, Callable, Generic, Iterator, TypeVar
from uuid import UUID, uuid4

T = TypeVar('T')
RT = TypeVar('RT')

logger = logging.getLogger(__name__)


class Alias:
    WORKER = 'WORKER'
    MAIN = 'MAIN'
    OTHER = 'OTHER'
    MANAGER = 'MANAGER'


def trace(process_alias, msg, *args, **kwargs):
    current_process = multiprocessing.current_process()
    logger.debug(f'[{process_alias}] {msg} ({current_process}, pid={os.getpid()})', *args, **kwargs)


class Status(Enum):
    READY = 1


class Job:
    id: UUID
    status: Status
    socket_file: Path

    task_fn: Callable

    listener: mc.Listener | None
    conns: list[mc.Connection]

    conn_listener: threading.Thread

    def __init__(
        self,
        job_id: UUID,
        socket_file: Path,
        task_fn: Callable,
        args: list,
        kwargs: dict,
    ) -> None:
        super().__init__()
        self.id = job_id
        self.status = Status.READY
        self.socket_file = socket_file
        self.task_fn = task_fn
        self.args = args
        self.kwargs = kwargs
        self.conns = []
        self.listener = None
        self.acceptor_started_event = threading.Event()

    def start_listening(self):
        trace(Alias.OTHER, 'socket path listener: %s', self.socket_file)
        self.listener = mc.Listener(str(self.socket_file), family='AF_UNIX')

        def acceptor(listener: mc.Listener, conns: list[mc.Connection], started: threading.Event):
            logger.debug('[WORKER] started listener for task id=%s', self.id)

            started.set()

            while True:
                conn = listener.accept()
                logger.debug('[WORKER] accepted conn: %s', conn)
                conns.append(conn)

        self.conn_listener = threading.Thread(
            target=acceptor, args=(self.listener, self.conns, self.acceptor_started_event), daemon=True
        )
        self.conn_listener.start()

    def notify(self, obj):
        for conn in self.conns:
            conn.send(obj)

    def start_work(self) -> Any:
        trace(Alias.WORKER, 'job starting for id=%s', self.id)

        started_evt = threading.Event()

        recv, send = multiprocessing.Pipe()

        def notifier(started, conn, job):
            started.set()

            while True:
                try:
                    job.notify(conn.recv())
                except EOFError:
                    break

        threading.Thread(target=notifier, args=(started_evt, recv, self), daemon=True).start()

        # XXX: arbitrary wait
        started_evt.wait(timeout=15)

        result = self.task_fn(*self.args, **self.kwargs, notifier=send)._getvalue()  # noqa

        return result

    def execute(self) -> Any:
        # TODO: this causes error
        self.start_listening()
        # self.acceptor_started_event.wait()
        return self.start_work()


@dataclass
class CecilyFuture(Generic[RT]):
    job_id: UUID
    socket_file: Path

    _future: concurrent.futures.Future

    def collect(self) -> Iterator[RT]:
        if not self._future.running:
            return

        with mc.Client(str(self.socket_file), family='AF_UNIX') as client:
            while True:
                yield client.recv()

    def result(self) -> Any:
        return self._future.result()


def worker(job_id, temp_socket_file, manager_sock, task_fn_name, args, kwargs):
    trace(Alias.WORKER, 'init new job with task_fn=%s id=%s', task_fn_name, job_id)

    manager = TaskManager(address='manager.sock')
    manager.register(task_fn_name)
    manager.connect()

    task_fn = getattr(manager, task_fn_name)

    job = Job(job_id, temp_socket_file, task_fn, args, kwargs)

    return job.execute()


@dataclass
class Task:
    app_ref: 'Cecily'
    task_fn: Callable

    def __call__(self, *args, **kwargs) -> CecilyFuture:
        trace(Alias.OTHER, 'task for task_fn=%s called', self.task_fn.__name__)

        # create id
        job_id = uuid4()

        # create pub/sub conn
        temp_socket_file: Path = self.app_ref.sock_dir / str(job_id)
        temp_socket_file = temp_socket_file.with_suffix('.sock')

        future = self.app_ref.executor.submit(
            worker,
            job_id,
            temp_socket_file,
            self.app_ref.manager_sock,
            self.task_fn.__name__,
            args,
            kwargs,
        )

        return CecilyFuture(job_id, temp_socket_file, future)


class TaskManager(BaseManager):
    pass


def manager_worker(deferred_functions, sock='manager.sock'):
    trace(Alias.MANAGER, 'starting')

    m = TaskManager(sock)

    for task in deferred_functions:
        logger.debug('[MANAGER] registering %s', task.__name__)
        m.register(task.__name__, task)

    trace(Alias.MANAGER, 'serving')
    s = m.get_server()
    s.serve_forever()


class Cecily:
    executor: ProcessPoolExecutor
    sock_dir: Path

    manager: TaskManager | None
    manager_sock: Path

    serialized_tasks: list[bytes]

    spawned: bool

    def __init__(self, max_workers: int | None = None) -> None:
        current_process = multiprocessing.current_process()

        # XXX: determines if this app is called from the Main app's ProcessPoolExecutor
        #   by checking if the current process is spawned
        if isinstance(current_process, multiprocessing.context.SpawnProcess):
            self.spawned = True
            trace(Alias.OTHER, 'skipping app init')
            return

        trace(Alias.MAIN, 'creating app')
        self.spawned = False
        self.executor = ProcessPoolExecutor(max_workers)
        self.sock_dir = Path(tempfile.mkdtemp())

        logger.debug('[MAIN] created sock dir: %s', self.sock_dir)
        self.manager_sock = self.sock_dir / 'manager.sock'
        self.manager_sock.touch(exist_ok=True)
        self.manager = TaskManager(address='manager.sock')

        self.deferred_functions = []
        self.manager_worker = multiprocessing.Process(
            target=manager_worker, args=(self.deferred_functions,), daemon=True
        )

    def start(self):
        if self.spawned:
            return

        logger.debug('[MAIN] starting app')
        self.manager_worker.start()

    def task(self, fn) -> Callable:
        if self.spawned:
            return fn

        logger.debug('[MAIN] registering new task: %s', fn.__name__)

        fn.apply = Task(self, fn)

        # TODO: no duplicate registers
        self.deferred_functions.append(fn)

        return fn

    def close(self):
        logger.debug('[MAIN] shutting down app')
        self.manager_worker.terminate()
        self.manager_worker.join(timeout=10)

        self.executor.shutdown(cancel_futures=True)

        shutil.rmtree(self.sock_dir)
        logger.debug('[MAIN] shutdown complete')
