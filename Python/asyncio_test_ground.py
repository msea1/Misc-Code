import asyncio as aio
from datetime import datetime
import logging
import sys
import threading
import time


# ## WRITING ## #
class Command:
    def __init__(self, source, cmd):
        self.source = source.upper()
        self.cmd = cmd.upper()

    def __str__(self):
        return "{} issued by {}".format(self.cmd, self.source)


def write_to_socket(cmd):
    """Mimic writing to serial"""
    s_log = logging.getLogger('Socket_Writer')
    s_log.info("Sent ~ {} ~ to {}".format(cmd, az_sock))
    s_log.info("Sent ~ {} ~ to {}".format(cmd, el_sock))


@aio.coroutine
def status_loop():
    while True:
        status_cmd = Command('Status_Loop', 'STATUS')
        yield from loop.run_in_executor(None, write_to_socket, status_cmd)
        yield from aio.sleep(1)


@aio.coroutine
def post_loop():
    while True:
        cmd = yield from queue.get()
        log.info('Post submitted {}'.format(cmd.cmd))
        yield from loop.run_in_executor(None, write_to_socket, cmd)


def get_user_cmd():
    """Equiv to commands coming from REST."""
    while True:
        user_input = input("Enter Command:\n")
        cmd = Command("Post", user_input)
        queue.put_nowait(cmd)


#    ### READING ###   #


def display_date(init_sleep, name):
    """Equiv to reading bytes from socket."""
    t_log = logging.getLogger(name)
    time.sleep(init_sleep)
    while True:
        timer = datetime.now()
        t_log.info('Running {} @ {}'.format(name, timer))
        loop.call_soon_threadsafe(ingest_msg, timer)
        time.sleep(2)


def ingest_msg(msg):
    """Models antenna updating itself per status"""
    a_log = logging.getLogger('Antenna')
    a_log.info('Updating status now @ {}'.format(msg))


@aio.coroutine
def spoof_blocking():
    """PoC that threadsafe calls waits for a yield"""
    while True:
        log.info('Blocking')
        time.sleep(4)
        log.info('Yielding from block')
        yield from aio.sleep(1)


logging.basicConfig(level=logging.INFO, format='%(threadName)10s %(name)18s: %(message)s', stream=sys.stderr)

queue = aio.Queue()
log = logging.getLogger()
loop = aio.get_event_loop()
az_sock = 'AZM'
el_sock = 'ELV'
tasks = [
    loop.create_task(status_loop()),
    loop.create_task(post_loop())
]
thr_post = threading.Thread(target=get_user_cmd).start()
thr_rad_a = threading.Thread(target=display_date, args=(0, 'AZM')).start()
thr_read_e = threading.Thread(target=display_date, args=(1, 'ELV')).start()
#loop.create_task(spoof_blocking())
loop.run_forever()
