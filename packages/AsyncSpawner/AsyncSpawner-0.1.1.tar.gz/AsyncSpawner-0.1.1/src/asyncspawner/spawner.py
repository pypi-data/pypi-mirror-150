import asyncio
from functools import partial
from threading import Thread, current_thread
from multiprocessing import Pipe, current_process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from .logger import get_logger


_logger = get_logger()


class AsyncSpawner:
    '''
    Initializes a new AsyncSpawner instance.

    Args:
        pr_max_workers: The maximum number of processes that can be used to
            execute the given calls. If None or not given then as many
            worker processes will be created as the machine has processors.
        pr_mp_context: A multiprocessing context to launch the workers. This
            object should provide SimpleQueue, Queue and Process.
        pr_initializer: A callable used to initialize worker processes.
        pr_initargs: A tuple of arguments to pass to the process initializer.
        th_max_workers: The maximum number of threads that can be used to
            execute the given calls.
        th_thread_name_prefix: An optional name prefix to give our threads.
        th_initializer: A callable used to initialize worker threads.
        th_initargs: A tuple of arguments to pass to the thread initializer.
        wait_executor: An optional concurrent.futures.ThreadPoolExecutor
            instance that is used to await for spawn call results. If None or
            not given then on every spawn call a new one with a single thread
            worker will be created.
        loop: An optional event loop instance. If None or not given then a
            currently running loop will be used.
    '''

    def __init__(
            self,
            pr_max_workers=None,
            pr_mp_context=None,
            pr_initializer=None,
            pr_initargs=(),
            th_max_workers=None,
            th_thread_name_prefix='',
            th_initializer=None,
            th_initargs=(),
            wait_executor=None,
            loop=None,
        ):
            initializer = AsyncSpawner._process_initializer(
                pr_initializer,
                max_workers=th_max_workers,
                thread_name_prefix=th_thread_name_prefix,
                initializer=th_initializer,
                initargs=th_initargs)

            self._process_executor = ProcessPoolExecutor(
                max_workers=pr_max_workers,
                mp_context=pr_mp_context,
                initializer=initializer,
                initargs=pr_initargs)

            self._wait_executor = wait_executor
            self._loop = loop or asyncio.get_running_loop()

    async def spawn(self, coro, *args, **kwargs):
        '''
        Submits a coroutine to be executed with the given arguments.

        Schedules the coroutine to be executed as coro(*args, **kwargs) and
        returns a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        '''
        coro = partial(coro, *args, **kwargs)

        pipe = await self._loop.run_in_executor(self._process_executor, AsyncSpawner._run_in_process, coro)
        task = await self._loop.run_in_executor(self._waiter, pipe.recv)

        try:
            raise task['exception']
        except KeyError:
            pass

        return task['result']

    @property
    def _waiter(self):
        return self._wait_executor or ThreadPoolExecutor(max_workers=1)

    @staticmethod
    def _process_initializer(fn, **kwargs):

        def wrapper(*args):
            proc = current_process()
            _logger.info(f'Initialize {proc.name}')

            proc.loop = asyncio.new_event_loop()
            proc.loop_runner = Thread(target=proc.loop.run_forever, daemon=True)
            proc.loop_runner.start()
            _logger.info(f'{proc.name} started event loop')

            proc.thread_executor = ThreadPoolExecutor(**kwargs)
            _logger.info(f'{proc.name} created thread pool')

            if callable(fn):
                fn(*args)

        return wrapper

    @staticmethod
    def _run_in_process(coro):
        proc = current_process()
        _logger.info(f'{proc.name} received task {coro}')

        proc_conn, task_conn = Pipe()

        coro = AsyncSpawner._run_coro(coro, task_conn)
        ft = proc.loop.run_in_executor(proc.thread_executor, AsyncSpawner._run_in_thread, coro)

        # Waiting for thread to accept the task:
        proc_conn.recv()

        def task_done_callback(ft):
            task = {'task': str(coro)}

            try:
                task['result'] = ft.result()
            except Exception as e:
                task['exception'] = e
                _logger.exception(f'{proc.name} failed to process task {coro}')
            finally:
                task_conn.send(task)
                _logger.info(f'{proc.name} finished {task}')

        ft.add_done_callback(task_done_callback)

        return proc_conn

    @staticmethod
    def _run_in_thread(coro):
        proc = current_process()
        thread = current_thread()
        _logger.info(f'{proc.name}::{thread.name} received task {coro}')

        ft = asyncio.run_coroutine_threadsafe(coro(), loop=proc.loop)

        return ft.result()

    @staticmethod
    def _run_coro(coro, task_conn):
        proc = current_process()

        async def wrapper():
            # Notify the parent process the task has been started:
            task_conn.send(True)

            thread = current_thread()
            _logger.info(f'{proc.name}:{thread.name} started task {coro}')

            return await coro()

        return wrapper
