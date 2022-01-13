import asyncio
import os
import shlex
import signal
from typing import Dict, Tuple

MAX_RETRIES = 2
RETRYABLE_RETURN_CODE = 449%256


# For non-blocking keyboard input.
def alarm_handler(_signum, _frame):
    raise Exception()


def step_succeeded(step_name: str):
    print(f'step {step_name} passed! onto next step')


def retry_step(step_name: str):
    print(f'step {step_name} failed for reasons that may succeed if we try again. replaying')


def step_failed(step_name: str):
    print(f'step {step_name} failed! log and stop workflow')


async def create_worker(s: str, workers: Dict, attempt_num: int = 0):
    # Dispatch a worker.
    print('dispatcher about to create worker')
    plugin, ttl = shlex.split(s)
    worker_process = await asyncio.create_subprocess_exec('python3', 'mock_worker.py', plugin, ttl)
    worker_future = asyncio.ensure_future(worker_process.wait())

    # Here create any worker object you want containing worker_process
    # and any other metadata about the worker.
    worker = (worker_process, worker_process.pid, plugin, ttl, attempt_num)
    workers[worker_future] = worker
    print('dispatcher created worker')

    if plugin == 'oom':
        literal_ttl = int(ttl) - 2
        kill_future = asyncio.ensure_future(asyncio.sleep(literal_ttl))
        workers[kill_future] = (worker_process, worker_process.pid, 'sigterm', literal_ttl, 0)


async def dispatcher():
    # For non-blocking keyboard input.
    signal.signal(signal.SIGALRM, alarm_handler)

    workers: Dict[asyncio.Future, Tuple[asyncio.subprocess.Process, int, str, int, int]] = {}

    done = False
    while not done:
        # This is a hackey way to get non-blocking keyboard input,
        # but good enough for this test code.
        s = None
        signal.alarm(1)
        try:
            s = input()
            signal.alarm(0)
        except Exception:
            pass

        if s == 'exit':
            done = True
        elif s:
            await create_worker(s, workers)

        # Check if any workers are completed.
        pending_futures = workers.keys()
        if pending_futures:
            completed_futures, _ = await asyncio.wait(pending_futures, timeout=0, return_when=asyncio.FIRST_COMPLETED)

            # Handle completed workers.
            for future in completed_futures:
                worker = workers.pop(future)
                print(f'dispatcher received completed worker {worker} with returncode {worker[0].returncode}')
                print(f'dispatcher has {len(workers)} pending workers')
                if worker[2] == 'sigterm':
                    # time to kill the referenced (worker[1]) job
                    os.kill(worker[1], signal.SIGTERM)
                elif worker[0].returncode == 0:
                    step_succeeded(worker[2])
                elif worker[0].returncode == RETRYABLE_RETURN_CODE:
                    if worker[4] >= MAX_RETRIES:
                        print(f'too many retries for {worker[2]}, time to die')
                        step_failed(worker[2])
                    else:
                        retry_step(worker[2])
                        retries = worker[4] + 1
                        await create_worker(f"{worker[2]} {worker[3]}", workers, retries)
                else:
                    step_failed(worker[2])


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dispatcher())

""" Examples
Connected to pydev debugger (build 201.8538.36)
georef 2
dispatcher about to create worker
dispatcher created worker
dispatcher has 1 pending workers
pydev debugger: process 10889 is connecting
worker executing georef for 2 seconds
worker executing georef, -3 seconds left
worker done executing georef
dispatcher received completed worker [<Process 10889>, 10889, 'georef'] with returncode 0
dispatcher has 0 pending workers
step georef passed! onto next step
oom 5
dispatcher about to create worker
dispatcher created worker
dispatcher has 1 pending workers
pydev debugger: process 10902 is connecting
worker executing oom for 5 seconds
dispatcher received completed worker [<Process 10902>, 10902, 'sigterm'] with returncode None
dispatcher has 1 pending workers
Destruct sequence from signal 15 completed and engaged. Goodbye
dispatcher received completed worker [<Process 10902>, 10902, 'oom'] with returncode 15
dispatcher has 0 pending workers
step oom failed! log and stop workflow
"""
