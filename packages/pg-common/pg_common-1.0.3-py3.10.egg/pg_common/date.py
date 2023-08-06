from datetime import datetime, timedelta


__all__ = ["datetime_now", "datetime_delta", "datetime_2_str", "datetime_2_timestamp",
           "str_delta_str", "str_2_datetime", "timestamp_2_str"]
__auth__ = "baozilaji@gmail.com"


def datetime_now():
    return datetime.now()


def datetime_delta(_date_time, _delta_hours=0):
    return _date_time + timedelta(hours=_delta_hours)


def datetime_2_str(_date_time_base, _delta_hours, _fmt="%Y-%m-%d %H:%M:%S"):
    return datetime_delta(_date_time_base, _delta_hours).strftime(_fmt)


def datetime_2_timestamp(_datetime):
    return datetime.timestamp(_datetime)


def str_delta_str(_str, _delta=0, _in_fmt="%Y-%m-%d %H:%M:%S", _out_fmt="%Y-%m-%d %H:%M:%S"):
    return (str_2_datetime(_str, _delta, _in_fmt)).strftime(_out_fmt)


def str_2_datetime(_str, _delta=0, _in_fmt="%Y-%m-%d %H:%M:%S"):
    return datetime_delta(datetime.strptime(_str, _in_fmt), _delta)


def timestamp_2_str(_timestamp, _fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(_timestamp).strftime(_fmt)

