import asyncio

from sdbus import (DbusInterfaceCommonAsync, dbus_method_async, dbus_property_async, dbus_signal_async,
                   request_default_bus_name_async)

"""
This script creates a dbus endpoint that you can interact with.

busctl --user introspect sand.box /sand/box
NAME                                TYPE      SIGNATURE RESULT/VALUE FLAGS
org.freedesktop.DBus.Introspectable interface -         -            -
.Introspect                         method    -         s            -
org.freedesktop.DBus.Peer           interface -         -            -
.GetMachineId                       method    -         s            -
.Ping                               method    -         -            -
org.freedesktop.DBus.Properties     interface -         -            -
.Get                                method    ss        v            -
.GetAll                             method    s         a{sv}        -
.Set                                method    ssv       -            -
.PropertiesChanged                  signal    sa{sv}as  -            -
sand.box.cmds                       interface -         -            -
.AsyncPing                          method    -         -            -
.DoubleInt                          method    i         i            -
.Echo                               method    -         -            -
.Ping                               method    -         s            -
.Update                             method    s         s            -
.SignalAlert                        signal    s         -            -


Calls can be make like:
busctl --user call sand.box /sand/box sand.box.cmds Ping
busctl --user call sand.box /sand/box sand.box.cmds AsyncPing
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
        self._string_prop = 'example'

    @dbus_method_async(result_signature='s')
    async def ping(self) -> str:
        return 'The world says hello'

    @dbus_method_async(result_signature='s')
    async def async_ping(self) -> str:
        await asyncio.sleep(1)
        return 'The world says hello, async'

    @dbus_method_async('s', 's')
    async def echo(self, what: str) -> str:
        return what

    @dbus_method_async(input_signature='i', result_signature='i')
    async def double_int(self, an_int: int) -> int:
        return an_int * 2

    @dbus_property_async('s')
    def string_prop(self) -> str:
        return self._string_prop

    @string_prop.setter
    def string_prop(self, new_str: str) -> None:
        self._string_prop = new_str

    @dbus_method_async('s', 's')
    async def update(self, message: str) -> str:
        resp = f'spreading the good word: {message}'
        self.signal_alert.emit(message)
        return resp

    @dbus_signal_async('s')
    async def signal_alert(self) -> str:
        raise NotImplementedError


ex = ExampleInterface()


async def start_example():
    """Perform async startup actions"""
    await request_default_bus_name_async(BUS_NAME)
    # Export the object to dbus
    ex.export_to_dbus(PATH)
    # wait indefinitely
    await asyncio.get_event_loop().create_future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_example())
