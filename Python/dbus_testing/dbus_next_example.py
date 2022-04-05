import asyncio

from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, Variant, dbus_property, method, signal

"""
This script creates a dbus endpoint that you can interact with.

busctl --user introspect sand.box /sand/box
NAME                                TYPE      SIGNATURE RESULT/VALUE FLAGS
org.freedesktop.DBus.Introspectable interface -          -             -
.Introspect                         method    -          s             -
org.freedesktop.DBus.ObjectManager  interface -          -             -
.GetManagedObjects                  method    -          a{oa{sa{sv}}} -
.InterfacesAdded                    signal    oa{sa{sv}} -             -
.InterfacesRemoved                  signal    oas        -             -
org.freedesktop.DBus.Peer           interface -          -             -
.GetMachineId                       method    -          s             -
.Ping                               method    -          -             -
org.freedesktop.DBus.Properties     interface -          -             -
.Get                                method    ss         v             -
.GetAll                             method    s          a{sv}         -
.Set                                method    ssv        -             -
.PropertiesChanged                  signal    sa{sv}as   -             -
sand.box.cmds                       interface -          -             -
.echo                               method    s          s             -
.ping                               method    -          s             -
.print_variant_dict                 method    -          a{sv}         -
.update                             method    s          s             -
.string_prop                        property  s          "example"     emits-change writable
.signal_alert                       signal    s          -             -


Calls can be make like:
busctl --user call sand.box /sand/box sand.box.cmds ping
busctl --user call sand.box /sand/box sand.box.cmds echo s 'hi.cfg'
busctl --user get-property sand.box /sand/box sand.box.cmds string_prop
busctl --user set-property sand.box /sand/box sand.box.cmds string_prop s 'example2'

Confirmation of signal can be done by running:
dbus-monitor --session --monitor "type='signal',interface='sand.box.cmds'"  # in terminal A
busctl --user call sand.box /sand/box sand.box.cmds update s 'cheese'  # in terminal B

and seeing the signal appear in terminal A
"""

BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


async def start_example():
    bus = await MessageBus().connect()
    interface = ExampleInterface(IFACE)
    bus.export(PATH, interface)
    # now that we are ready to handle requests, we can request name from D-Bus
    found_name = await bus.request_name(BUS)
    print(f'Found dbus: {found_name}')
    # wait indefinitely
    await asyncio.get_event_loop().create_future()


class ExampleInterface(ServiceInterface):
    def __init__(self, name):
        super().__init__(name)
        self._string_prop = 'example'

    @method()
    def ping(self) -> 's':
        return 'The world says hello'

    @method()
    async def async_ping(self) -> 's':
        await asyncio.sleep(0.25)
        return 'The world says hello'

    @dbus_property()
    def string_prop(self) -> 's':
        return self._string_prop

    @string_prop.setter
    def string_prop(self, val: 's'):
        self._string_prop = val

    @method()
    def echo(self, what: 's') -> 's':
        return what

    @method()
    def update(self, message: 's') -> 's':
        resp = f'spreading the good word: {message}'
        self.signal_alert(message)
        return resp

    @signal()
    def signal_alert(self, message: 's') -> 's':
        return message

    @method()
    def print_variant_dict(self) -> 'a{sv}':
        return {
            'foo': Variant('s', 'bar'),
            'bat': Variant('x', -55),
            'a_list': Variant('as', ['hello', 'world'])
        }


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_example())
