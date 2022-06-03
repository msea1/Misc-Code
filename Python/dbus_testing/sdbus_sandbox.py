import asyncio
from typing import Any

from sdbus import (DbusInterfaceCommonAsync, dbus_method_async, dbus_signal_async, request_default_bus_name_async)

"""
This script creates a dbus endpoint that you can interact with.

busctl --user introspect sand.box /sand/box

Calls can be make like:
busctl --user call sand.box /sand/box sand.box.cmds Ping
busctl --user call sand.box /sand/box sand.box.cmds Echo s 'hi.cfg'
busctl --user call sand.box /sand/box sand.box.cmds DoubleInt i 5

Confirmation of signal can be done by running:
dbus-monitor --session --monitor "type='signal',interface='sand.box.cmds'"  # in terminal A
busctl --user call sand.box /sand/box sand.box.cmds Update s 'cheese'  # in terminal B

and seeing the signal appear in terminal A
"""

BUS_NAME = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


class ExampleInterface(DbusInterfaceCommonAsync, interface_name=IFACE):
    def __init__(self):
        super().__init__()

    @dbus_method_async('s', 's')
    async def update(self, message: str) -> str:
        resp = f'spreading the good word: {message}'
        self.signal_alert.emit(message)
        desired_msg = [
            ('svc_a', {"sap_a": ('y', 3), "sap_b": ('b', True)}),
            ('svc_b', {"sap_c": ('d', 3.3), "sap_b": ('b', True)}),
            ('svc_c', {"sap_d": ('u', 0), "sap_b": ('b', True)}),
        ]
        self.signal_alert2.emit(desired_msg)
        return resp

    @dbus_method_async('ya(sv)')
    async def multi(self, _image: int, updates: list[str, str, str]) -> None:
        saps = {}
        for sap_key, (dbus_type, sap_value) in updates:
            print(f"updating {sap_key} to {sap_value} from dbus type {dbus_type}")
            saps[sap_key] = (dbus_type, sap_value)
        desired_msg = [
            ('svc_a', saps),
            ('svc_b', saps),
        ]
        self.signal_alert2.emit(desired_msg)

    @dbus_signal_async('s')
    async def signal_alert(self) -> str:
        raise NotImplementedError

    @dbus_signal_async('a(sa{sv})')
    async def signal_alert2(self) -> list[tuple[str, dict[str, tuple[str, Any]]]]:
        """
        a( = list (of tuples)
            s = str
            a{ = dict
                s = str
                v = variant, denoted by tuple of [
                    DBus type (string), value (Any)
                ]
            }
        )
        """
        raise NotImplementedError


serve_ex = ExampleInterface()
proxy_ex = ExampleInterface.new_proxy(BUS_NAME, PATH)


async def start_example():
    """Perform async startup actions"""
    await request_default_bus_name_async(BUS_NAME)
    # Export the object to dbus
    serve_ex.export_to_dbus(PATH)


async def clock() -> None:
    while True:
        await serve_ex.update('ping')
        await asyncio.sleep(5)


async def print_alert1() -> None:
    async for x in proxy_ex.signal_alert:
        print('Got alert 1: ', x)


async def print_alert2() -> None:
    async for x in proxy_ex.signal_alert2:
        print('Got alert 2!')
        for r in x:
            print(f'service {r[0]}')
            print(f'updates {r[1]}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_example())
    # loop.create_task(print_alert1())
    # loop.create_task(print_alert2())
    # loop.create_task(clock())
    loop.run_forever()
