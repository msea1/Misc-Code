import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

"""
This script creates a dbus endpoint that you can interact with.

busctl --user introspect sand.box /sand/box
NAME                                TYPE      SIGNATURE RESULT/VALUE FLAGS
org.freedesktop.DBus.Introspectable interface -         -            -
.Introspect                         method    -         s            -
sand.box.cmds                       interface -         -            -
.parrot                             method    s         s            -
.ping                               method    -         s            -
.send_args                          method    s(ddd)    s            -
.update                             method    s         s            -
.signal_alert                       signal    as        -            -


Calls can be make like:
busctl --user call sand.box /sand/box sand.box.cmds ping
busctl --user call sand.box /sand/box sand.box.cmds parrot s 'hi.cfg'
busctl --user call sand.box /sand/box sand.box.cmds send_args s\(ddd\) hi 2.2 3.3 4.4

Confirmation of signal can be done by running:
dbus-monitor --session --monitor "type='signal',interface='sand.box.cmds'"  # in terminal A
busctl --user call sand.box /sand/box sand.box.cmds update s 'cheese'  # in terminal B

and seeing the signal appear in terminal A
"""

BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


def start_emulator():
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    # despite not being referenced herein, the BusName has to be assigned to a variable, otherwise
    # something in the system bus will not register it.
    # as a requirement of dbus binding
    _name = dbus.service.BusName(BUS, session_bus)
    Emulator(session_bus, PATH)

    mainloop = GLib.MainLoop()

    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()


class Emulator(dbus.service.Object):
    def __init__(self, bus, obj_path):
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
        v1, v2, v3 = vector
        resp = f'{word} saw vector: {v1}, {v2}, & {v3}'
        return resp

    @dbus.service.method(IFACE, in_signature='s', out_signature='s')
    def update(self, message):
        resp = f'spreading the good word: {message}'
        self.signal_alert(message)
        return resp

    @dbus.service.signal(IFACE, signature='as')
    def signal_alert(self, message):
        pass


if __name__ == "__main__":
    start_emulator()
