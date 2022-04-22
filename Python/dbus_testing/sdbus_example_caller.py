import asyncio

from sdbus_example_interface import BUS_NAME, ExampleInterface, PATH

ex = ExampleInterface.new_proxy(BUS_NAME, PATH)


async def test():
    print(await ex.async_ping())
    print(await ex.double_int(5))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.run_forever()
