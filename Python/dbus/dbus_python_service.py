import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


class Parrot(dbus.service.Object):
    def __init__(self, bus):
        super().__init__(bus, PATH)

    @dbus.service.method(IFACE, in_signature='as', out_signature='as')
    def Ack(self, msg):
        print(msg);
        beep = [f'{msg[0]}:1', f'{msg[1]}:4.5']
        self.AckSignal(beep)
        return beep

    @dbus.service.signal(IFACE, signature='as')
    def AckSignal(self, message):
        pass


def main():
    print('Hello')
    DBusGMainLoop(set_as_default=True)
    system_bus = dbus.SessionBus()
    bus_name = dbus.service.BusName(BUS, system_bus)
    dbus_object = Parrot(system_bus)

    mainloop = GLib.MainLoop()

    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()


if __name__ == '__main__':
    main()

