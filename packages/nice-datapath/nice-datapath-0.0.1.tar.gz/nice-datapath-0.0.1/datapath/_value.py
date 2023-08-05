import re
from typing import Any

from datapath._pipe import get_pipe


def value(data: Any, path: str) -> Any:
    if not path:
        return data

    pipes = path.split("|")
    keys = pipes[0].split(".")
    pipes = pipes[1:]

    for k in keys:
        k = k.strip()
        data = __value(data, k)

    for pipe in pipes:
        pipe = pipe.strip()
        params = re.split(r"\s+", pipe)
        data = get_pipe(params[0])(data, *params[1:])

    return data


def __value(data: Any, key: str) -> Any:
    if isinstance(data, dict):
        return data[key]

    if isinstance(data, (list, tuple, set)):
        return [__value(item, key) for item in data]

    return getattr(data, key)
