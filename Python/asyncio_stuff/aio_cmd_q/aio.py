import asyncio
import logging.config
import random
import sys

from cmdseq.utils import get_epoch_time

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s : %(message)s")
TIMEOUT = 1


class TestBox:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.script_queue = asyncio.Queue()
        self.script_task = None
        self.script_task_sleep = None
        self.cmd_queue = asyncio.Queue()
        self.running = True

        self.loop.create_task(self.exec_script())
        self.loop.create_task(self.exec_cmds())
        self.start_time = get_epoch_time()
        self.last_scripted_cmd_ended = None

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    @staticmethod
    def stop():
        for task in asyncio.Task.all_tasks():
            task.cancel()

    async def sample_cmd(self, arg):
        log.info(f'running command {arg} at {int(self.get_relative_time())}')
        await asyncio.sleep(random.random()/1000)  # mimic ops
        return str(f"{arg} has finished")

    async def sample_long_cmd(self, arg):
        log.info(f'running command {arg} at {int(self.get_relative_time())}')
        await asyncio.sleep(.3)  # mimic ops
        return str(f"{arg} has finished")

    def send_resp(self, msg):
        log.info(f"RESP: {msg} at {int(self.get_relative_time())}")

    def log_resp(self, msg):
        log.info(f"LOG: {msg} at {int(self.get_relative_time())}")

    def get_message(self, message_dict):
        cmd_list = message_dict['commands']
        if message_dict['type'] == 'packet':
            self.add_commands(cmd_list)
        else:
            self.add_script(cmd_list)

    def add_commands(self, cmd_list):
        log.info(f'{len(cmd_list)} command(s) added via packet')
        for x in cmd_list:
            self.cmd_queue.put_nowait((x[0], x[1], 0 if x[1] == 'now' else x[2]))

    def add_script(self, script):
        self.cancel_old_script()
        log.info(f'{len(script)} command(s) added via script')
        for x in script:
            self.script_queue.put_nowait((x[0], x[1], 0 if x[1] == 'now' else x[2]))

    def cancel_old_script(self):
        log.info(f'{self.script_queue.qsize()} command(s) removed from queue')
        if self.script_task_sleep:
            log.info(f'A waiting command has been cancelled.')
            self.loop.call_soon_threadsafe(self.script_task_sleep.cancel)
        if self.script_task:
            log.info(f'A running command has been cancelled.')
            self.loop.call_soon_threadsafe(self.script_task.cancel)
        while self.script_queue.qsize() > 0:
            self.script_queue.get_nowait()
            self.script_queue.task_done()

    def get_relative_time(self):
        return (get_epoch_time() - self.start_time) * 10

    async def sleep_and_await_cancellation(self, sleepy_time):
        await asyncio.sleep(sleepy_time)
        return True

    async def await_cmd_finish(self, cmd_to_run):
        resp = await cmd_to_run
        return resp

    def _make_command(self, cmd_name):
        return self.sample_long_cmd(cmd_name) if 'long_cmd' in cmd_name else self.sample_cmd(cmd_name)

    async def handle_cmd_timing(self, rel_sec_to_sleep):
        proceed = True
        try:
            self.script_task_sleep = self.loop.create_task(self.sleep_and_await_cancellation(rel_sec_to_sleep))
            proceed = await self.script_task_sleep
        except asyncio.CancelledError:
            log.debug('Caught cancellation as expected during sleep')
            proceed = False
        except:
            proceed = False
        finally:
            self.script_task_sleep = None
            return proceed

    async def handle_cmd_exec(self, cmd_to_run):
        cmd_resp = ''
        try:
            self.script_task = self.loop.create_task(self.await_cmd_finish(cmd_to_run))
            cmd_resp = await self.script_task
        except asyncio.CancelledError:
            log.debug('Caught cancellation as expected during execution')
            cmd_resp = 'Cancelled during execution'
        finally:
            self.script_task = None
            return cmd_resp

    async def exec_script(self):
        log.info(f'Script consumer started at {int(self.get_relative_time())}')
        script_resp = ''
        while True:
            await self.cmd_queue.join()  # blocks until queue is empty
            task_name, time_method, time_sec = await self.script_queue.get()
            rel_sec_to_sleep = self._get_sleep_time(time_method, time_sec)
            log.debug(f"EVAL {task_name}, relative time is {int(self.get_relative_time())}")
            log.debug(f"SLEEP for {rel_sec_to_sleep*10} and then run {task_name}")
            try:
                if rel_sec_to_sleep < 0:
                    raise Exception(f'{task_name} task is in the past and will be skipped')
                to_proceed = await self.handle_cmd_timing(rel_sec_to_sleep)
                if not to_proceed:
                    log.error('Told not to proceed')
                    script_resp = 'Cancelled'
                    continue

                script_cmd = self._make_command(task_name)
                log.debug(f"RUN {task_name}, relative time is now {int(self.get_relative_time())}")
                script_resp = await self.handle_cmd_exec(script_cmd)
                log.debug(f"FINISH {task_name}, relative time is now {int(self.get_relative_time())}")
            except Exception as e:
                log.error(str(e))
                script_resp = str(e)
            finally:
                log.debug(f"Calling task done on {task_name}. Queue is {self.script_queue.qsize()}")
                self.script_queue.task_done()
                self.last_scripted_cmd_ended = int(self.get_relative_time())
                self.log_resp(script_resp)

    async def exec_cmds(self):
        log.info(f'Command consumer started at {int(self.get_relative_time())}')
        cmd_resp = ''
        while True:
            task_name, _, _ = await self.cmd_queue.get()
            log.debug(f"about to eval {task_name}, relative time is {int(self.get_relative_time())}")
            try:
                # check s/c mode TODO
                cmd_task = self._make_command(task_name)
                log.debug(f"about to run {task_name}, relative time is now {int(self.get_relative_time())}")
                cmd_resp = await asyncio.wait_for(cmd_task, TIMEOUT)
                log.debug(f"about to finish {task_name}, relative time is now {int(self.get_relative_time())}")
            except Exception as e:
                log.error(str(e))
                cmd_resp = str(e)
            finally:
                self.cmd_queue.task_done()
                self.send_resp(cmd_resp)

    def _get_sleep_time(self, method, time_sec):
        if method.lower() == 'now':
            return 0
        elif method.lower() == 'absolute':
            adj_time = time_sec
            sleep_step = adj_time - int(self.get_relative_time())
            return sleep_step / 10
        elif method.lower() == 'relative':
            if self.last_scripted_cmd_ended is None:
                return 0
            rel_time_exec = self.last_scripted_cmd_ended + time_sec
            est_exec = (rel_time_exec - int(self.get_relative_time())) / 10
            return est_exec if est_exec > 0 else 0


class ACG:
    """ Tries to join the cmd_queue. Which will be blocked until the queue is processed.
    then the acg can join, and put some stuff into the queue.
    Hopefully, that handles disconnecting ACG when stuff is in the queue and also allows
    queue consumer to use await queue.get()
    """
    def __init__(self, cmdr):
        self.cmds = 0
        self.cmdr = cmdr
        self.internal_checks_to_make = 5

    # transform into pull model where it checks for track station else returns tracks sun? TODO
    async def run(self):
        while True:
            if not self.cmdr.running:
                return
            cmd_checks_made = 0
            log.debug(f"ACG reset. Checks made now {cmd_checks_made}")
            await self.cmdr.script_queue.join()  # blocks until queue is empty
            await self.cmdr.cmd_queue.join()  # blocks until queue is empty
            log.debug(f"ACG finds nothing in queue at {int(self.cmdr.get_relative_time())}")
            while cmd_checks_made < self.internal_checks_to_make:
                if not self.cmdr.running:
                    return
                elif self.queues_are_empty():
                    cmd_checks_made += 1
                    log.debug(f"ACG checked at {int(self.cmdr.get_relative_time())}, checks made now {cmd_checks_made}")
                    await asyncio.sleep(.1)
                    log.debug(f"ACG slept until {int(self.cmdr.get_relative_time())}, checks still at {cmd_checks_made}")
                else:
                    break  # cmd_checks_made reset to 0
            if (cmd_checks_made == self.internal_checks_to_make) and self.queues_are_empty():
                self.cmdr.add_commands([self.mock_now_acg_command()])

    def queues_are_empty(self):
        return self.cmdr.cmd_queue.qsize() == 0 and self.cmdr.script_queue.qsize() == 0

    def mock_now_acg_command(self):
        self.cmds += 1
        return f'acg_cmd_{self.cmds}', 'now'

    def mock_acg_command(self):
        self.cmds += 1
        return f'acg_cmd_{self.cmds}_rel', 'relative', random.randint(10, 120)
