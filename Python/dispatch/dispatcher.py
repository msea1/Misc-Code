import asyncio
import os
import shlex
import signal
from typing import Dict, List, Union


# For non-blocking keyboard input.
def alarm_handler(*args):
    raise Exception()


def step_succeeded(step_name: str):
    print(f'step {step_name} passed! onto next step')


def step_failed(step_name: str):
    print(f'step {step_name} failed! log and stop workflow')


async def dispatcher():
    # For non-blocking keyboard input.
    signal.signal(signal.SIGALRM, alarm_handler)

    workers: Dict[asyncio.Future, List[Union[asyncio.subprocess.Process, int, str]]] = {}

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
            # Dispatch a worker.
            print('dispatcher about to create worker')
            worker_process = await asyncio.create_subprocess_exec('python3', 'worker.py', *shlex.split(s))
            worker_future = asyncio.ensure_future(worker_process.wait())

            # Here create any worker object you want containing worker_process
            # and any other metadata about the worker.
            plugin, ttl = s.split()
            worker = [worker_process, worker_process.pid, plugin]
            workers[worker_future] = worker
            print('dispatcher created worker')
            print(f'dispatcher has {len(workers)} pending workers')

            if plugin == 'oom':
                kill_future = asyncio.ensure_future(asyncio.sleep(int(ttl)-2))
                workers[kill_future] = [worker_process, worker_process.pid, 'sigterm']

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
                    os.kill(worker[1], signal.SIGTERM)
                else:
                    step_succeeded(worker[2]) if worker[0].returncode == 0 else step_failed(worker[2])


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dispatcher())
