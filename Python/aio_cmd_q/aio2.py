import asyncio
import logging.config
import random
import sys

from cmdseq.utils import get_epoch_time

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
TIMEOUT = 5


class TestBox:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.script_queue = asyncio.Queue()
        self.running = True
        self.loop.set_debug(enabled=True)  # TODO: remove before production

        self.start_time = get_epoch_time()
        self.loop_task = self.loop.create_task(self.exec_script())
        self.last_scripted_cmd_ended = None

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    def stop(self):
        self.loop_task.cancel()

    async def sample_cmd(self, arg):
        log.info(f'running command {arg} at {int(self.get_relative_time())}')
        await asyncio.sleep(random.random()/1000)  # mimic ops
        return str(f"{arg} has finished")

    async def sample_long_cmd(self, arg):
        log.info(f'running command {arg} at {int(self.get_relative_time())}')
        await asyncio.sleep(3)  # mimic ops
        return str(f"{arg} has finished")

    def log_resp(self, result):
        log.info(f"LOG: {result} at {int(self.get_relative_time())}")

    def get_message(self, message_dict):
        cmd_list = message_dict['commands']
        self.add_script(cmd_list)

    def add_script(self, script):
        log.info(f'{self.script_queue.qsize()} command(s) removed from queue')
        while self.script_queue.qsize() > 0:
            self.script_queue.get_nowait().cancel()
        log.info(f'{len(script)} command(s) added via script')
        for x in script:
            self.script_queue.put_nowait((x[0], x[1], 0 if x[1] == 'now' else x[2]))

    def get_relative_time(self):
        return get_epoch_time() - self.start_time

    async def exec_script(self):
        log.info(f'Script consumer started at {self.get_relative_time()}')
        cmd_resp = ''
        while True:
            task_name, time_method, time_sec = await self.script_queue.get()
            rel_sec_to_sleep = self._get_sleep_time(time_method, time_sec)
            log.debug(f"about to eval {task_name}, relative time is {int(self.get_relative_time())}")
            log.debug(f"sleep for {rel_sec_to_sleep} and then run {task_name}")
            try:
                if rel_sec_to_sleep < 0:
                    raise Exception('task is in the past')
                await asyncio.sleep(rel_sec_to_sleep)

                if 'long_cmd' in task_name:
                    script_task = self.sample_long_cmd(task_name)
                else:
                    script_task = self.sample_cmd(task_name)
                log.debug(f"about to run {task_name}, relative time is now {int(self.get_relative_time())}")
                cmd_resp = await asyncio.wait_for(script_task, TIMEOUT)
                log.debug(f"about to finish {task_name}, relative time is now {int(self.get_relative_time())}")
            except Exception as e:
                log.exception(e)
                cmd_resp = str(e)
            finally:
                self.script_queue.task_done()
                self.last_scripted_cmd_ended = self.get_relative_time()
                self.log_resp(cmd_resp)

    def _get_sleep_time(self, method, time_sec):
        if method.lower() == 'now':
            return 0
        elif method.lower() == 'absolute':
            return time_sec - self.get_relative_time()
        elif method.lower() == 'relative':
            rel_time_exec = self.last_scripted_cmd_ended + time_sec
            return rel_time_exec - self.get_relative_time()

