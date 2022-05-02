from typing import Callable

import asyncio
from time import monotonic

start_time = 0


async def repeat(func: Callable, interval_sec: float, *args, **kwargs) -> None:
    """Run func every interval_sec seconds.

    If func has not finished before *interval_sec*, will run again
    immediately when the previous iteration finished.
    """
    while True:
        await asyncio.gather(func(*args, **kwargs), asyncio.sleep(interval_sec))


async def f():
    global start_time
    await asyncio.sleep(1)
    print(f'Hello @ {round(monotonic() - start_time, 1)}')


async def g():
    global start_time
    await asyncio.sleep(0.5)
    print(f'Goodbye @ {round(monotonic() - start_time, 1)}')


async def h(input_str: str):
    global start_time
    await asyncio.sleep(0.5)
    print(f'{input_str} @ {round(monotonic() - start_time, 1)}')


async def automated():
    t1 = asyncio.create_task(repeat(f, 3), name="hello")
    t2 = asyncio.create_task(repeat(g, 2), name="goodbye")
    await asyncio.gather(t1, t2)


async def add_repeat():
    while True:
        inp = await asyncio.get_event_loop().run_in_executor(None, input, '\nEnter a keyword: ')
        asyncio.create_task(repeat(h, 1, input_str=inp))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    start_time = monotonic()
    loop.create_task(automated())
    loop.create_task(add_repeat())
    loop.run_forever()
