import dbus
import time
from threading import Thread
from dbus_python import start_emulator

BUS = 'sand.box'
PATH = '/sand/box'
IFACE = 'sand.box.cmds'


def main():
    connection_attempts = 0
    remote_object = None
    bus = dbus.SystemBus()
    print("Attempting to connect to {} for ADCS".format(BUS))
    while not remote_object and connection_attempts < 5:
        connection_attempts += 1
        try:
            remote_object = bus.get_object(BUS, PATH)
            break
        except dbus.DBusException as e:
            if 'ServiceUnknown' in e.get_dbus_name():  # fire emulator
                Thread(target=start_emulator, daemon=True).start()
                time.sleep(.05)  # give it a blink to publish
                bus = dbus.SessionBus()  # emulator is published to the session bus
            else:
                raise e
    dbus_iface = dbus.Interface(remote_object, IFACE)
    print('Emulator ready. Ctrl-C to quit.')
    print('Sending "DONE" shuts down the emulator.')

    while True:
        try:
            cmd = input(">: ")
            if cmd == 'DONE':
                print('Shutting down.')
                break
            else:
                if cmd.strip().lower() == 'ping':
                    print(dbus_iface.ping())
                elif cmd.strip().lower() == 'parrot':
                    words = input("Enter a message >: ")
                    print(dbus_iface.parrot(words))
                elif cmd.strip().lower() == 'send_args':
                    word = input("Enter a word >: ")
                    vector = input("Enter a target vector >: ")
                    target_vector = vector.split()
                    geodetic_vector = [float(d) for d in target_vector]
                    print(dbus_iface.send_args(word, geodetic_vector))
                else:
                    print('Unknown command encountered: {}'.format(cmd))
        except KeyboardInterrupt:
            print('Shutting down.')
            break


if __name__ == '__main__':
    main()

