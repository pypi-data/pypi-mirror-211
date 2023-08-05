import json
from typing import Any, Callable, Dict

__pipes: Dict[str, Callable] = {
    "str": lambda v: str(v),
    "int": lambda v: int(v),
    "float": lambda v: float(v),
    "jsondump": lambda v: json.dumps(v),
    "jsonload": lambda v: json.loads(v),
    "%": lambda v, prec=None: __pipe_percent(v, prec),
}


def register_pipe(name: str, fn: Callable):
    __pipes[name] = fn


def get_pipe(name: str):
    return __pipes[name]


def __pipe_percent(v: Any, prec=None):
    v = "{}".format(v * 100)

    if prec:
        prec = int(prec)
        cur_prec = 0
        i = v.find(".")
        if i >= 0:
            cur_prec = len(v) - i - 1
        if cur_prec < prec:
            if cur_prec == 0:
                v += "."
            v += "0" * (prec - cur_prec)
        if cur_prec > prec:
            v = v[:prec - cur_prec]
            v = v.strip(".")
    else:
        if "." in v:
            while v[-1] == "0":
                v = v[:-1]
            v = v.strip(".")

    return v + "%"
