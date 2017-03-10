With the main service running or the adcs/demo running, you can introspect the dbus
 ```bash
busctl --user introspect sand.box /sand/box
```
And call the methods on it with commands like
```bash
busctl --user call sand.box /sand/box sand.box.cmds ping
busctl --user call sand.box /sand/box sand.box.cmds parrot s 'hi.cfg'
busctl --user call sand.box /sand/box sand.box.cmds send_args s\(ddd\) hi 2.2 3.3 4.4
```
And see the corresponding output.

To see the service process an ADCS command:
 * Start the emulator as a background process
 * Start the caller demo
 * Follow prompts
