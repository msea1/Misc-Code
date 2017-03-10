from gi.repository import GLib
from pydbus import SessionBus

"""
A class to emulate the responses
"""

BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


def start_emulator():
    loop = GLib.MainLoop()
    emulator_class = get_emulator()
    emulator_class.__doc__ = emulator_class.__doc__.replace("{dbus_interface_name}", IFACE)
    new_obj = publish(BUS, emulator_class)

    try:
        loop.run()
    finally:
        new_obj.unpublish()
        exit(0)


def publish(bus_path, emulator):
    print('publishing {} on {}'.format(emulator, bus_path))
    bus = SessionBus()
    return bus.publish(bus_path, emulator())


def get_emulator():
    # this needs to track the adcs API
    class Emulator:
        """
            <node>
                <interface name='{dbus_interface_name}'>
                    <method name='parrot'>
                        <arg type='d' name='word' direction='in'/>
                        <arg type='s' name='response' direction='out'/>
                    </method>
                    <method name='ping'>
                        <arg type='s' name='response' direction='out'/>
                    </method>
                    <method name='send_args'>
                        <arg type='s' name='word' direction='in'/>
                        <arg type='(ddd)' name='vector' direction='in'/>
                        <arg type='s' name='response' direction='out'/>
                    </method>                    
                </interface>
            </node>
        """

        def __init__(self):
            self.target_type = ''
            self.current_task = ''

        @staticmethod
        def parrot(word):
            return word

        @staticmethod
        def ping():
            return "hello, world"

        def send_args(self, word, vector):
            self.current_task = 'args'
            v1, v2, v3 = vector
            resp = self.ping()
            return resp

    return Emulator
