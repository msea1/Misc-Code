import asyncio
import json
import logging
from os import getcwd
from os.path import join

import asyncssh


class Tasker:
    def __init__(self, loop):
        self.existing_track_task = None
        self.ssh = None
        self.home_directory = getcwd()
        self.loop = loop
        self.attempt_num = 0

        self.loop.run_until_complete(self.main())

    async def main(self):
        self.ssh = await asyncssh.connect('localhost', username='mcarruth', password='Seahawks12!')
        await self.track()
        print("tasker started")
        await asyncio.sleep(3)

        self.attempt_num += 1
        print("trying to track again")
        await self.track()
        await asyncio.sleep(2)

    async def track(self):
        await self.maybe_cancel_existing_task()
        self.existing_track_task = await self.execute_track()

    async def maybe_cancel_existing_task(self):
        if self.existing_track_task and not self.existing_track_task.done():
            print("Existing track not completed. Cancelling so we can start a new one")
            self.existing_track_task.cancel()
            try:
                print("awaiting cancel")
                await self.existing_track_task
                print("cancel done")
            except asyncio.CancelledError:
                print("CANCEL INSIDE MAYBE TASK")
        else:
            print("no issues with existing task")

    async def execute_track(self):
        return asyncio.ensure_future(self.execute_cli())

    async def execute_cli(self):
        cli_name = join(self.home_directory, 'controller.py')
        print(cli_name)
        async with self.ssh.create_process(f"python3 {cli_name} -n {self.attempt_num}", term_type='ansi', stdin=asyncssh.DEVNULL) as ssh_process:
            asyncio.ensure_future(self.log(ssh_process.stdout, ssh_process.command, logging.INFO))
            asyncio.ensure_future(self.log(ssh_process.stderr, ssh_process.command, logging.ERROR))
            await ssh_process.wait()
            print(f"execute_cli process finished with exit code: {ssh_process.exit_status}")

    @staticmethod
    async def log(ssh_reader, command, level):
        async for line in ssh_reader:
            extra_data = {'command': command}
            log_level = level
            log_line = line

            try:
                data = json.loads(line)
                log_line = data.get('message', line)
                log_level = data.get('level', level)

                extra_data.update({
                    f'async_ssh_test_{key}': value
                    for key, value in data.items()
                })
            except json.JSONDecodeError:
                pass

            print(f'{log_level}: Remote: {log_line}')


looper = asyncio.get_event_loop()
print("starting")
t = Tasker(looper)

