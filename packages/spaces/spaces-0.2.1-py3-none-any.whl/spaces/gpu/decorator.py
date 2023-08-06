"""
"""
from __future__ import annotations

import inspect
from typing import Callable
from typing import Generator
from typing import overload

from .wrappers import _Param
from .wrappers import _Res
from .wrappers import regular_function_wrapper
from .wrappers import generator_function_wrapper


already_decorated: set[Callable] = set()


@overload
def GPU(
    task:
     Callable[_Param, _Res],
) -> Callable[_Param, _Res]:
    ...
@overload
def GPU(
    task:
     Callable[_Param, Generator[_Res, None, None]],
) -> Callable[_Param, Generator[_Res, None, None]]:
    ...
def GPU(
    task:
      Callable[_Param, _Res]
    | Callable[_Param, Generator[_Res, None, None]],
) -> (Callable[_Param, _Res]
    | Callable[_Param, Generator[_Res, None, None]]):
    """
    """

    if task in already_decorated:
        return task

    if inspect.iscoroutinefunction(task):
        raise NotImplementedError

    if inspect.isgeneratorfunction(task):
        decorated = generator_function_wrapper(task)
    else:
        decorated = regular_function_wrapper(task)

    already_decorated.add(decorated)

    return decorated # type: ignore
