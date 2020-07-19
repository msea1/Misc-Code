import os
import signal
import sys
import time


def worker():
    plugin = sys.argv[1]
    time_left = int(sys.argv[2])
    print(f'worker executing {plugin} for {time_left} seconds')
    while time_left > 0:
        time.sleep(min(5, time_left))
        time_left -= 5
        print(f'worker executing {plugin}, {time_left} seconds left')
    print(f'worker done executing {plugin}')
    if plugin == 'fail':
        sys.exit(-1)
    sys.exit(0)


def die_gracefully(signum, _frame):
    # we get sigterm
    print(f'Destruct sequence from signal {signum} completed and engaged. Goodbye')
    try:
        pass  # maybe need to do something
    finally:
        sys.exit(signum)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, die_gracefully)
    worker()

