'''
装饰器
'''

import time
from ..logger import logger

def func_run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        logger.info('{} cost {}s'.format(func.__name__, end - start))
        return res
    return wrapper

if __name__=="__main__":
    @func_run_time
    def func(i):
        time.sleep(i)

    func(2)
