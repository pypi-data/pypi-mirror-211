"""
"""
from __future__ import annotations

from typing import Callable
from typing import Generator
from typing import overload

from . import utils
from .gpu.decorator import _Param
from .gpu.decorator import _Res
from .gpu.decorator import GPU


gradio_auto_wrap_disabled = False


def disable_gradio_auto_wrap():
    global gradio_auto_wrap_disabled
    gradio_auto_wrap_disabled = True


@overload
def gradio_auto_wrap(
    task:
     Callable[_Param, _Res],
) -> Callable[_Param, _Res]:
    ...
@overload
def gradio_auto_wrap(
    task:
     Callable[_Param, Generator[_Res, None, None]],
) -> Callable[_Param, Generator[_Res, None, None]]:
    ...
@overload
def gradio_auto_wrap(
    task:
     None,
) -> None:
    ...
def gradio_auto_wrap(
    task:
      Callable[_Param, _Res]
    | Callable[_Param, Generator[_Res, None, None]]
    | None,
) -> (Callable[_Param, _Res]
    | Callable[_Param, Generator[_Res, None, None]]
    | None):
    """
    """
    if gradio_auto_wrap_disabled:
        return task
    if not callable(task):
        return task
    if utils.is_zero_gpu():
        return GPU(task) # type: ignore
    return task
