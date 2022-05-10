import asyncio

from sdbus_example_interface import BUS_NAME, ExampleInterface, PATH

ex = ExampleInterface.new_proxy(BUS_NAME, PATH)


async def print_alert1() -> None:
    # Use async for loop to print clock signals we receive
    async for x in ex.signal_alert:
        print('Got alert 1: ', x)


async def print_alert2() -> None:
    # Use async for loop to print clock signals we receive
    async for x in ex.signal_alert2:
        print('Got alert 2')
        print(f'service is: {x[0]}')
        print(f'args are: {x[1]}')


async def test():
    print(await ex.async_ping())
    print(await ex.double_int(5))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(print_alert1())
    loop.create_task(print_alert2())
    # loop.run_until_complete(test())
    loop.run_forever()
