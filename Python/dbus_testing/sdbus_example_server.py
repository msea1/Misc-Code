import asyncio

from sdbus import request_default_bus_name_async

from sdbus_example_interface import BUS_NAME, ExampleInterface, PATH

ex = ExampleInterface()


async def start_example():
    """Perform async startup actions"""
    await request_default_bus_name_async(BUS_NAME)
    # Export the object to dbus
    ex.export_to_dbus(PATH)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_example())
    loop.run_forever()
