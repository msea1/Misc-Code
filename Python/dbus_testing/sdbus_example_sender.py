import asyncio
from dataclasses import dataclass
from typing import Any

from sdbus import DbusInterfaceCommonAsync, dbus_method_async, request_default_bus_name_async

BUS_NAME = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'

# ######### SAMPLE SAPs ######### #
SAPS = {
    "test.1": {
        "name": "test.1",
        "type": "uint16",
        "value": 5
    },
    "test.2": {
        "name": "test.2",
        "type": "boolean",
        "value": True  # has to be of correct type here, cannot be 0 or 1
    }
}
# ######### SAMPLE SAPs ######### #
DBUS_TYPES = {
    "boolean": "b",
    "uint16": "q",
    "string": "s"
}


@dataclass(slots=True)
class SapVariant:
    name: str
    type: str
    value: Any


class ExampleInterface(DbusInterfaceCommonAsync, interface_name=IFACE):
    def __init__(self):
        super().__init__()
        self.saps = {
            k: SapVariant(k, v["type"], v["value"]) for k, v in SAPS.items()
        }

    @dbus_method_async(result_signature='a{sv}')
    async def read_all(self) -> dict:
        resp = {s.name: (DBUS_TYPES[s.type], s.value) for s in self.saps.values()}
        print(resp)  # {'test.1': ('q', 5), 'test.2': ('b', True)} --> a{sv} 2 "test.1" q 5 "test.2" b true
        return resp

    @dbus_method_async(result_signature='v')
    async def read_variant(self) -> tuple:
        sap = self.saps['test.1']
        resp = DBUS_TYPES[sap.type], sap.value
        print(resp)  # ('q', 5) --> v q 5
        return resp

    @dbus_method_async(result_signature='a{sb}')
    async def read_dict(self) -> dict:
        resp = {s.name: bool(s.value) for s in self.saps.values()}
        print(resp)  # {'test.1': True, 'test.2': True} --> a{sb} 2 "test.1" true "test.2" true
        return resp


ex = ExampleInterface()


async def start_example():
    """Perform async startup actions"""
    await request_default_bus_name_async(BUS_NAME)
    # Export the object to dbus
    ex.export_to_dbus(PATH)
    # wait indefinitely
    await asyncio.get_event_loop().create_future()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_example())
