"""
"""
from __future__ import annotations

import multiprocessing
import os
import signal
import traceback
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pickle import PicklingError
from threading import Thread
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Generator
from typing import Generic
from typing import TypeVar
from typing_extensions import ParamSpec

import psutil

from ..utils import drop_params
from ..utils import SimpleQueue as Queue
from . import client
from . import torch


Process = multiprocessing.get_context('fork').Process

_Arg = tuple[tuple[Any], dict[str, Any]]
_Res = TypeVar('_Res')
_Param = ParamSpec('_Param')


class Worker(Generic[_Res]):
    process: Process
    arg_queue: Queue[_Arg]
    res_queue: Queue[_Res]
    _sentinel: Thread

    def __init__(
        self,
        target: Callable[[Queue[_Arg], Queue[_Res], list[int]], None],
    ):
        self._sentinel = Thread(target=self._close_on_exit)
        self.arg_queue = Queue()
        self.res_queue = Queue()
        fds = [c.fd for c in psutil.Process().connections()]
        args = self.arg_queue, self.res_queue, fds
        if TYPE_CHECKING:
            target(*args)
        self.process = Process(
            target=target,
            args=args,
            daemon=True,
        )

    def start(self):
        self.process.start()
        self._sentinel.start()

    def _close_on_exit(self):
        self.process.join()
        self.res_queue.close()


def regular_function_wrapper(
    task:
     Callable[_Param, _Res],
) -> Callable[_Param, _Res]:

    worker: Worker[list[_Res] | Exception] | None = None

    def process_wrapper(*args: _Param.args, **kwargs: _Param.kwargs) -> _Res:
        print("process_wrapper")
        nonlocal worker
        if worker is None or not worker.process.is_alive():
            worker = Worker(thread_wrapper)
            worker.start()
        schedule_response = client.schedule()
        release = partial(client.release, nvidia_index=schedule_response.nvidiaIndex)
        try:
            worker.arg_queue.put((args, kwargs))
        except PicklingError:
            release(fail=True)
            raise
        try:
            res = worker.res_queue.get()
        except EOFError:
            release(fail=True)
            raise RuntimeError("Operation aborted")
        if isinstance(res, Exception):
            release(fail=True)
            raise res
        release()
        return res[0]


    def thread_wrapper(
        arg_queue: Queue[_Arg],
        res_queue: Queue[list[_Res] | Exception],
        fds: list[int],
    ):
        torch.unpatch()
        torch.move(0)
        for fd in fds:
            os.close(fd)
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        while True:
            try:
                args, kwargs = arg_queue.get()
            except OSError:
                break
            with ThreadPoolExecutor() as executor:
                future = executor.submit(task, *args, **kwargs)
            try:
                res = [future.result()]
            except Exception as e:
                traceback.print_exc()
                res = e
            try:
                res_queue.put(res)
            except PicklingError as e:
                res_queue.put(e)
    
    return process_wrapper


def generator_function_wrapper(
    task:
     Callable[_Param, Generator[_Res, None, None]],
) -> Callable[_Param, Generator[_Res, None, None]]:

    worker: Worker[list[_Res] | Exception | None] | None = None

    def process_wrapper(*args: _Param.args, **kwargs: _Param.kwargs) -> Generator[_Res, None, None]:
        print("process_wrapper")
        nonlocal worker
        if worker is None or not worker.process.is_alive():
            worker = Worker(thread_wrapper)
            worker.start()

        schedule_response = client.schedule()
        release = partial(client.release, nvidia_index=schedule_response.nvidiaIndex)

        try:
            worker.arg_queue.put((args, kwargs))
        except PicklingError:
            release(fail=True)
            raise

        yield_queue: Queue[list[_Res] | Exception | None] = Queue()
        def fill_yield_queue(worker: Worker[list[_Res] | Exception | None]):
            while True:
                try:
                    res = worker.res_queue.get()
                except Exception:
                    release(fail=True)
                    yield_queue.close()
                    return
                if isinstance(res, Exception):
                    release(fail=True)
                    yield_queue.put(res)
                    return
                if res is None:
                    release()
                    yield_queue.put(None)
                    return
                yield_queue.put(res)

        with ThreadPoolExecutor() as e:
            e.submit(fill_yield_queue, worker)
            while True:
                try:
                    res = yield_queue.get()
                except Exception:
                    raise RuntimeError("Operation aborted")
                if isinstance(res, Exception):
                    raise res
                if res is None:
                    break
                yield res[0]


    def thread_wrapper(
        arg_queue: Queue[_Arg],
        res_queue: Queue[list[_Res] | Exception | None],
        fds: list[int],
    ):
        torch.unpatch()
        torch.move(0)
        for fd in fds:
            os.close(fd)
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        while True:
            try:
                args, kwargs = arg_queue.get()
            except OSError:
                break
            def iterate():
                gen = task(*args, **kwargs) # type: ignore
                while True:
                    try:
                        res = next(gen)
                    except StopIteration:
                        break
                    except Exception as e:
                        res_queue.put(e)
                        break
                    try:
                        res_queue.put([res])
                    except PicklingError as e:
                        res_queue.put(e)
                        break
                    else:
                        continue
            with ThreadPoolExecutor() as executor:
                executor.submit(iterate)
            res_queue.put(None)

    return process_wrapper
