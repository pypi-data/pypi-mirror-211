"""
"""

import os
from http import HTTPStatus

import requests
from pydantic import BaseModel

from .. import utils


NODE_IP = os.environ['NODE_IP'] # Fail if not defined
BASE_URL = f"http://{NODE_IP}:8000"
CGROUP_PATH = utils.self_cgroup_device_path()


class ScheduleParams(BaseModel):
    cgroupPath: str

class ScheduleResponse(BaseModel):
    idle: bool
    nvidiaIndex: int

class ReleaseParams(BaseModel):
    cgroupPath: str
    nvidiaIndex: int
    fail: bool


def post(path: str, params: BaseModel) -> requests.Response:
    print(f'{params.dict()=}')
    return requests.post(BASE_URL + path, params=params.dict())


def schedule() -> ScheduleResponse:

    res = post('/schedule', params=ScheduleParams(
        cgroupPath=CGROUP_PATH,
    ))

    if res.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise RuntimeError("GPU already in use")

    try:
        data = res.json()
    except requests.JSONDecodeError: # pragma: no cover
        data = {}

    if not res.ok: # pragma: no cover
        raise RuntimeError(f"ZeroGPU API /schedule error: {data.get('detail')}")

    return ScheduleResponse(**data)


def release(nvidia_index: int, fail: bool = False) -> None:

    res = post('/release', params=ReleaseParams(
        cgroupPath=CGROUP_PATH,
        nvidiaIndex=nvidia_index,
        fail=fail,
    ))

    if not res.ok:
        try:
            data = res.json()
        except requests.JSONDecodeError: # pragma: no cover
            data = {}
        raise RuntimeError(f"ZeroGPU API /release error: {data.get('detail')}")

    return None
