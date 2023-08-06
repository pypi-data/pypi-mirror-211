# 用装饰器方法异步执行
import threading


def threaded_execution(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper
