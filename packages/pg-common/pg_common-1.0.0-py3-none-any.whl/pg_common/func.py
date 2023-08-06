import asyncio
from .date import datetime_now


def merge_dict(_to, _from):
    if _to and _from and isinstance(_to, dict) and isinstance(_from, dict):
        for _key, _value in _to.items():
            if _key in _from:
                _fv = _from[_key]
                if type(_value) == type(_fv):
                    if type(_value) == dict:
                        merge_dict(_value, _fv)
                    else:
                        _to[_key] = _fv
        for _key in _from:
            if _key not in _to:
                _to[_key] = _from[_key]


def log_print(tag, msg):
    print(f"{datetime_now()} - {tag} - {msg}")


def start_coroutines(_all_coroutines):
    if _all_coroutines:
        _temp = None
        if isinstance(_all_coroutines, list):
            _temp = _all_coroutines
        else:
            _temp = [_all_coroutines]

        for _c in _temp:
            if asyncio.iscoroutinefunction(_c):
                _c = _c()

            if not asyncio.iscoroutine(_c):
                raise ValueError(f"parameter must be coroutine instance, now is {type(_c)}")

            asyncio.create_task(_c)

