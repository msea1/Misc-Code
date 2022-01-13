import signal
import sys
import time

import numpy as np

from tests_dioptra.demo.dispatch_demo import RETRYABLE_RETURN_CODE


def worker():
    plugin = sys.argv[1]
    time_left = int(sys.argv[2])
    print(f'worker executing {plugin} for {time_left} seconds')
    while time_left > 0:
        time_to_sleep = min(5, time_left)
        busy_wait(time_to_sleep)
        time_left -= time_to_sleep
        print(f'worker executing {plugin}, {time_left} seconds left')
    print(f'worker done executing {plugin}')
    if plugin == 'fail':
        sys.exit(-1)
    elif plugin == 'retry':
        sys.exit(RETRYABLE_RETURN_CODE)
    sys.exit(0)


def die_gracefully(signum, _frame):
    # we get sigterm
    print(f'Destruct sequence from signal {signum} completed and engaged. Goodbye')
    try:
        pass  # maybe want to do something
    finally:
        sys.exit(signum)


def busy_wait(delay_seconds):
    """Just so the PID will show up in `top` as consuming some CPU and MEM"""
    data = np.arange(10000000, dtype=np.uint64)
    for _ in range(delay_seconds):
        data = np.invert(data)
        time.sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, die_gracefully)
    worker()
