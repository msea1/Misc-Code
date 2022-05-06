import asyncio
from dataclasses import dataclass
from typing import Any

import sdbus
from sdbus import (DbusInterfaceCommonAsync, dbus_method_async, dbus_property_async, dbus_signal_async)

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


@dataclass
class PersistedKeyValue:
    key_name: str
    key_value: str
    data_type: str


PERSISTENT_DATA_CACHE = {1: {}}
booted_image = 1
DBUS_DATA_TYPE_CONVERSIONS = {
    # plain text data type to DBus native type designator and lambda to convert to it
    "boolean": ('b', lambda x: bool(x)),
    "uint8": ('y', lambda x: int(x)),
    "uint16": ('q', lambda x: int(x)),
    "uint32": ('u', lambda x: int(x)),
    "uint64": ('t', lambda x: int(x)),
    "int8": ('y', lambda x: int(x)),
    "int16": ('n', lambda x: int(x)),
    "int32": ('i', lambda x: int(x)),
    "int64": ('x', lambda x: int(x)),
    "float": ('d', lambda x: float(x)),
    "float32": ('d', lambda x: float(x)),
    "float64": ('d', lambda x: float(x)),
    "string": ('s', lambda x: str(x)),
}


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

    @dbus_method_async(input_signature="sa(sv)")
    async def set_persistent_list(self, service_name: str, new_entries: list[str, tuple[str, Any]]) -> None:
        # busctl --user call sand.box /sand/box sand.box.cmds SetPersistentList "sa(sv)" hi 1 two y 2
        data_cache = PERSISTENT_DATA_CACHE[booted_image]
        for (key_name, (dbus_type, key_value)) in new_entries:
            full_name = f"{service_name}.{key_name}"
            if full_name not in data_cache:
                data_cache[full_name] = PersistedKeyValue(full_name, key_value, dbus_type)
                print(f"Create new persistent data store: {data_cache[full_name]}")
            else:
                print(f"Updating persistent data store for {full_name} from {data_cache[full_name].key_value} to {key_value}")
                data_cache[full_name].key_value = key_value

    @dbus_method_async(input_signature='sas', result_signature='a{sv}')
    async def read_persistent_list(self, service_name: str, key_names: list[str]) -> dict:
        # busctl --user call sand.box /sand/box sand.box.cmds ReadPersistentList "sas" hi 2 one two
        data_cache = PERSISTENT_DATA_CACHE[booted_image]
        resp = {}
        for key_name in key_names:
            full_name = f"{service_name}.{key_name}"
            if full_name not in data_cache:
                raise sdbus.DbusFailedError(f"{full_name} does not exist in persistent data store")
            else:
                entry: PersistedKeyValue = data_cache[full_name]
                resp[key_name] = (entry.data_type, entry.key_value)
        print(resp)  # {'one': ('y', 3), 'two': ('y', 2)}
        return resp
