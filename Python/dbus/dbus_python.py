import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

"""
A class to emulate the responses
"""

BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


def start_emulator():
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName(BUS, session_bus)
    object = Emulator(session_bus, PATH)

    mainloop = GLib.MainLoop()

    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()


class Emulator(dbus.service.Object):

    def __init__(self, bus, obj_path):
        self.current_task = ''
        super().__init__(bus, obj_path)

    @dbus.service.method(IFACE, in_signature='s', out_signature='s')
    def parrot(self, file_name):
        return file_name

    @dbus.service.method(IFACE, in_signature='', out_signature='s')
    def ping(self):
        resp = 'The world says hello'
        return resp

    @dbus.service.method(IFACE, in_signature='s(ddd)', out_signature='s')
    def send_args(self, word, vector):
        self.current_task = 'args'
        v1, v2, v3 = vector
        resp = self.ping()
        return resp


if __name__ == "__main__":
    start_emulator()
