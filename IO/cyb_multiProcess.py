#from __future__ import absolute_import
from . import hello
from . import cyb_decorator
from ..logger import logger
from multiprocessing import Process, Pool
import os

class MultiRun(object):
    def __init__(self, func, args:list, num_process=3) -> list:
        '''
        --------------------------
        input
        --------------------------
        func: 需要多进程执行的函数
        args: 传入func参数
        num_process: 并行数量
        --------------------------
        output
        --------------------------
        res: list, func 返回结果的 list
        --------------------------
        '''
        self.func = func
        self.args = args
        self.num_process = num_process

    def run_1(self):
        '''
        Pool map
        返回结果是有序的
        '''
        with Pool(self.num_process) as p:
            #print(p.map(self.func, self.args))
            return p.map(self.func, self.args)

    def run(self):
        '''
        Pool.apply_async, 可以对返回的结果增加一层处理函数，callback
        '''
        if self.num_process < 2:
            logger.warning('num_process less than 2, run 1 job...')
            return [self.func(arg) for arg in self.args]
        p = Pool(self.num_process)
        res_all = []
        def extend_res(res):
            res_all.extend(res)
        task_block = len(self.args) // self.num_process + 1
        for i in range(self.num_process):
            p.apply_async(self.process, args=(i, self.func, self.args[i * task_block : min((i + 1) * task_block, len(self.args))]), callback=extend_res)
        #p_pools = [Process(target=self.func, args=(self.args[i * task_block : min((i + 1) * task_block, len(self.args))])) for i in range(self.num_process)]
        #return [p.start() for p in p_pools]
        p.close()
        p.join()
        return res_all

    def process(self, task_i, func, args):
        logger.info('task {} start'.format(task_i))
        res = []
        for arg in args:
            res.append(func(arg))
        logger.info('task {} done!'.format(task_i))
        return res


if __name__=='__main__':
    import time
    import random
    random.seed(2019)

    @cyb_decorator.func_run_time
    def func(s):
        time.sleep(random.randint(10, 100) / 100.)
        print(s)
        return s

    #print(type(func))
    MR = MultiRun(func, [i for i in range(10)], num_process=3)
    #res= MR.run()
    #print(res)
    MR.run_1()
