import os
import sys
import time
import threading
import socket
import multiprocessing
from functools import wraps
from vllm.logger import init_logger

logger = init_logger(__name__)



# 1. Gather system, process, and thread metadata
hostname = socket.gethostname()
    
# Get the process name (falls back to script name if it's the main process)
proc_name = multiprocessing.current_process().name
if proc_name == "MainProcess" and sys.argv:
  proc_name = os.path.basename(sys.argv[0])


def trace_start(name, tid=None):
  logger.info("trace-start-event: name={} ts={} pid={}/{}/{} tid={}".format(name, time.time(), hostname, proc_name, os.getpid(), tid or threading.get_ident()))

def trace_end(name, tid=None):
  logger.info("trace-end-event: name={} ts={} pid={}/{}/{} tid={}".format(name, time.time(), hostname, proc_name, os.getpid(), tid or threading.get_ident()))



def trace_event(func):
    # 1. Gather system, process, and thread metadata
    hostname = socket.gethostname()
        
    # Get the process name (falls back to script name if it's the main process)
    proc_name = multiprocessing.current_process().name
    if proc_name == "MainProcess" and sys.argv:
        proc_name = os.path.basename(sys.argv[0])

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Get process and thread info
        pid = os.getpid()
        tid = threading.get_ident()

        # 2. Generate the start timestamp (seconds.nanoseconds)
        now_ns = time.time()

        # Print start trace
        logger.info(f'trace-start-event: name={func.__name__} ts={now_ns} pid={hostname}/{proc_name}/{pid} tid={tid}')

        # 3. Execute the actual function
        result = func(*args, **kwargs)

        # 4. Generate the end timestamp
        now_ns = time.time()

        # Print end trace
        logger.info(f'trace-end-event: name={func.__name__} ts={now_ns} pid={hostname}/{proc_name}/{pid} tid={tid}')
        
        return result
    return wrapper
