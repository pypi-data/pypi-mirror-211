"""Includes helper functions used for multiprocessing/multithreading."""
from threading import Thread
from typing import List, Callable, Any, Optional

from joblib import Parallel, delayed


def execute_parallel(_list: Optional[List[Any]], func: Callable, num_jobs=-1, backend: str = None,
                     require_shared_memory: bool = False, prefer_threads: bool = None,
                     **kwargs):
    """
    Runs given 'func' multiple times using given number of threads/processes, with elements in '_list' as arguments.

    :param _list: Includes arguments for every execution of 'func'. That is, func will be run len(_list) times.
    :param func: Function to execute in parallel.
    :param num_jobs: Number of threads/processes to use
    :param backend: 'joblib' library backend type to use.Values: loky(default), threading, multiprocessing
    :param require_shared_memory: Should be true if methods use a shared variable.
    :param prefer_threads: If true, it hints that func can efficiently use threads.
    :param kwargs:
    :return: Results of 'func' in the order according to arguments in _list.
    """
    require = "sharedmem" if require_shared_memory else None
    prefer = None
    if prefer_threads:
        prefer = "threads"
    args_list = []
    for arg in _list:
        if not isinstance(arg, tuple):
            arg = (arg,)
        args_list.append(arg)
    return Parallel(n_jobs=num_jobs, backend=backend, require=require, prefer=prefer, **kwargs)(
        delayed(func)(*args) for args in args_list)


def execute_multithreaded(_list: List[Any], func: Callable, num_threads=None):
    """
    Runs given 'func' multiple times using given number of threads, with elements in '_list' as arguments

    :param _list: Includes arguments for every executiın of 'func'. That is, func will be run len(_list) times.
    :param func: Function to execute in parallel.
    :param num_threads: Number of threads to use to execute 'func' in parallel.
    """
    list_len = len(_list)
    if num_threads is None:
        num_threads = list_len
    num_threads = min(num_threads, list_len)
    all_threads = []
    index = 0
    step = int(list_len / num_threads)
    remainder = list_len % num_threads
    for i in range(num_threads):
        last_index = index + step
        if remainder != 0 and i < remainder:
            last_index += 1
        arg_lists = _list[index: last_index]
        thread = Thread(target=__exec_multiple, args=(func, arg_lists))
        thread.start()
        all_threads.append(thread)
        index = last_index
    for thr in all_threads:
        thr.join()


def __exec_multiple(func, arg_lists):
    for arg_list in arg_lists:
        func(*arg_list)
