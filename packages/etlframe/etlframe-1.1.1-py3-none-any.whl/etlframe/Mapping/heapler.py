import json

from sqlalchemy.engine import CursorResult
import time
import functools


def get_records(result: CursorResult, batch_size: int, columns) -> list:
    """
    按照batch_size返回结果，结果返回迭代器
    :param result: sqlalchemy 的结果
    :param batch_size:
    :param columns:
    :return:
    """
    records = result.fetchmany(batch_size)
    while records:
        if isinstance(columns, list):
            records = [dict(zip(columns, i)) for i in records]
        if isinstance(columns, dict):
            records = [dict(zip(columns.keys(), i)) for i in records]
        for record in records:
            # print(record)
            yield record
        records = result.fetchmany(batch_size)


class Singleton(type):

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


def limit_iterator(rows, limit):
    for i, r in enumerate(rows):
        if i < limit:
            yield r
        else:
            return None


def validate_param(name, value, type_or_types):
    if isinstance(value, type_or_types):
        return value
    else:
        raise ValueError(f"{name} 参数错误")


def lower_columns(x):
    if isinstance(x, (list, tuple)):
        return tuple([i.lower() for i in x])
    else:
        return x.lower()


def batch_dataset(dataset, batch_size):
    cache = []
    for data in dataset:
        cache.append(data)
        if len(cache) >= batch_size:
            yield cache
            cache = []
    if cache:
        yield cache


def print_run_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        cost = time.time() - start
        cost = round(cost, 3)
        print(f"{func.__name__}函数执行了{cost}s")
        return r

    return wrapper

def dict_to_json(d:dict):
    return json.dumps(d, ensure_ascii=False)

@print_run_time
def main():
    pass


