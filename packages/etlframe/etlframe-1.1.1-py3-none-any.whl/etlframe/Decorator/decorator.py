import json
import sys
import threading
import time
import traceback
from collections import namedtuple
from functools import wraps
from inspect import getattr_static

from nb_log import LogManager

handle_exception_log = LogManager('function_error').get_logger_and_add_handlers()


## 时间装饰器
def run_many_times(times=1):
    """把函数运行times次的装饰器
    :param times:运行次数
    没有捕获错误，出错误就中断运行，可以配合handle_exception装饰器不管是否错误都运行n次。
    """

    def _run_many_times(func):
        @wraps(func)
        def __run_many_times(*args, **kwargs):
            for i in range(times):
                print('* ' * 50 + '当前是第 {} 次运行[ {} ]函数'.format(i + 1, func.__name__))
                func(*args, **kwargs)

        return __run_many_times

    return _run_many_times


def method_register(cls, is_rewrite_func=True):
    """
    类添加方法和修改方法， 无论类中是否存在该方法都会复写该方法，主要用于修改一些第三方库，需要添加功能又或者需要修改里面的逻辑
    用法：
    class A():
        def __init__(self):
            self.name = "A"

        def info(self):
            print('self.name--修改前', self.name)

    @method_register(A, is_rewrite_func=False)
    def info(self):
        print('self.name--修改后', self.name)

    obj = A()
    obj.info()
    :param cls:
           is_now_func: bool
                        True  重写该方法
                        False 不重写该方法
    :return:
    """

    def decorator(func):
        if is_rewrite_func:
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            setattr(cls, func.__name__, wrapper)
            return func

    return decorator


def return_dict_to_object_by_namedtuple(result_object: object):
    def namedtuple_inner(func):
        """
        首先建立一个返回的全局对象的命令空间，为了pycharm可以联想
        Result = namedtuple('Result', ['x', 'y', 'c'])
        结果如果是dict，返回Result的对象
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                result: result_object = result_object(**result)
            else:
                return result
            return result

        return wrapper

    return namedtuple_inner


def return_dict_to_object(func):
    """
    不需要联想，直接返回对象,转字典可以使用_toDict()
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            Result = namedtuple('Result', result)
            globals()['Result'] = Result
            result: Result = Result(**result)
        else:
            return result
        return result

    return wrapper


def handle_exception(retry_times=0, error_detail_level=0, is_throw_error=False, time_sleep=0):
    """捕获函数错误的装饰器,重试并打印日志
    :param retry_times : 重试次数
    :param error_detail_level :为0打印exception提示，为1打印3层深度的错误堆栈，为2打印所有深度层次的错误堆栈
    :param is_throw_error : 在达到最大次数时候是否重新抛出错误
    :type error_detail_level: int
    """

    if error_detail_level not in [0, 1, 2]:
        raise Exception('error_detail_level参数必须设置为0 、1 、2')

    def _handle_exception(func):
        @wraps(func)
        def __handle_exception(*args, **keyargs):
            for i in range(0, retry_times + 1):
                try:
                    result = func(*args, **keyargs)
                    if i:
                        handle_exception_log.debug(
                            u'%s\n调用成功，调用方法--> [  %s  ] 第  %s  次重试成功' % ('# ' * 40, func.__name__, i))
                    return result

                except Exception as e:
                    error_info = ''
                    if error_detail_level == 0:
                        error_info = '错误类型是：' + str(e.__class__) + '  ' + str(e)
                    elif error_detail_level == 1:
                        error_info = '错误类型是：' + str(e.__class__) + '  ' + traceback.format_exc(limit=3)
                    elif error_detail_level == 2:
                        error_info = '错误类型是：' + str(e.__class__) + '  ' + traceback.format_exc()

                    handle_exception_log.exception(
                        u'%s\n记录错误日志，调用方法--> [  %s  ] 第  %s  次错误重试， %s\n' % ('- ' * 40, func.__name__, i, error_info))
                    if i == retry_times and is_throw_error:  # 达到最大错误次数后，重新抛出错误
                        raise e
                time.sleep(time_sleep)

        return __handle_exception

    return _handle_exception


def synchronized(func):
    """线程锁装饰器，可以加在单例模式上"""
    func.__lock__ = threading.Lock()

    @wraps(func)
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


def singleton(cls):
    """
    单例模式装饰器,新加入线程锁，更牢固的单例模式，主要解决多线程如100线程同时实例化情况下可能会出现三例四例的情况,实测。
    """
    _instance = {}
    singleton.__lock = threading.Lock()

    @wraps(cls)
    def _singleton(*args, **kwargs):
        with singleton.__lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kwargs)
            return _instance[cls]

    return _singleton


def flyweight(cls):
    """
    享源装饰器
    :param cls:
    :return:
    """
    _instance = {}

    def _make_arguments_to_key(args, kwds):
        key = args
        if kwds:
            sorted_items = sorted(kwds.items())
            for item in sorted_items:
                key += item
        return key

    # @synchronized
    @wraps(cls)
    def _flyweight(*args, **kwargs):
        cache_key = f'{cls}_{_make_arguments_to_key(args, kwargs)}'
        if cache_key not in _instance:
            _instance[cache_key] = cls(*args, **kwargs)
        return _instance[cache_key]

    return _flyweight


def timer(func):
    """计时器装饰器，只能用来计算函数运行时间"""
    if not hasattr(timer, 'log'):
        timer.log = LogManager(f'timer_{func.__name__}').get_logger_and_add_handlers(
            log_filename=f'timer_{func.__name__}.log')

    @wraps(func)
    def _timer(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        t_spend = round(t2 - t1, 2)
        timer.log.debug('执行[ {} ]方法用时 {} 秒'.format(func.__name__, t_spend))
        return result

    return _timer


def where_is_it_called(func):
    """一个装饰器，被装饰的函数，如果被调用，将记录一条日志,记录函数被什么文件的哪一行代码所调用"""
    if not hasattr(where_is_it_called, 'log'):
        where_is_it_called.log = LogManager('where_is_it_called').get_logger_and_add_handlers()

    # noinspection PyProtectedMember
    @wraps(func)
    def _where_is_it_called(*args, **kwargs):
        # 获取被调用函数名称
        # func_name = sys._getframe().f_code.co_name
        func_name = func.__name__
        # 什么函数调用了此函数
        which_fun_call_this = sys._getframe(1).f_code.co_name  # NOQA

        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno

        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename

        # noinspection PyPep8
        where_is_it_called.log.debug(
            f'文件[{func.__code__.co_filename}]的第[{func.__code__.co_firstlineno}]行即模块 [{func.__module__}] 中的方法 [{func_name}] 正在被文件 [{file_name}] 中的'
            f'方法 [{which_fun_call_this}] 中的第 [{line}] 行处调用，传入的参数为[{args},{kwargs}]')
        try:
            t0 = time.time()
            result = func(*args, **kwargs)
            result_raw = result
            t_spend = round(time.time() - t0, 2)
            if isinstance(result, dict):
                result = json.dumps(result)
            if len(str(result)) > 200:
                result = str(result)[0:200] + '  。。。。。。  '
            where_is_it_called.log.debug('执行函数[{}]消耗的时间是{}秒，返回的结果是 --> '.format(func_name, t_spend) + str(result))
            return result_raw
        except Exception as e:
            where_is_it_called.log.debug('执行函数{}，发生错误'.format(func_name))
            where_is_it_called.log.exception(e)
            raise e

    return _where_is_it_called


class cached_class_property(object):
    """类属性缓存装饰器"""

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(cls, self.func.__name__, value)
        return value


def cached_method_result(fun):
    """方法的结果装饰器,不接受self以外的多余参数，主要用于那些属性的property方法属性上，这是同时缓存给类和实例。
    配合property装饰器，主要是在pycahrm自动补全上比上面的cached_property装饰器好"""

    @wraps(fun)
    def inner(self):
        if not hasattr(fun, 'result'):
            result = fun(self)
            fun.result = result
            fun_name = fun.__name__
            setattr(self.__class__, fun_name, result)
            setattr(self, fun_name, result)
            return result
        else:
            return fun.result

    return inner


if __name__ == '__main__':
    pass
