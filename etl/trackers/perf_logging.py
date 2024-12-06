"""Performance logging module"""

# Author: Daniel Broboana <daniel.broboana@gmail.com>

import os
import time
from functools import wraps

import psutil



def performace_logging(method):
    """
    Decorator to log the performance of a method, tracking execution
    time and memory usage.

    Logs:
        - `exec_time`: Execution time in seconds.
        - `memory_used`: Change in memory usage in bytes.
        - `transformer`: Name of the class where the method is defined.

    The log is stored as a list of dictionaries in the `traker_perf_log`
    attribute of the class.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        m0 = process.memory_info().rss
        t0 = time.perf_counter()
        results = method(*args, **kwargs)
        t = time.perf_counter() - t0
        m = process.memory_info().rss  - m0
        mdata = [{
            'transformer': args[0].__class__.__name__,
            'exec_time': t,
            'memory_used': m
        }]
        setattr(args[0].__class__, 'traker_perf_log', mdata)
        return results
    return wrapper
