import asyncio
import unittest

from cmdseq.sandbox.aio2 import TestBox


class TestCommander(unittest.TestCase):
    def setUp(self):
        self.cmdr = TestBox()
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.cmdr.running = False
        self.loop.run_until_complete(self.cmdr.script_queue.join())  # clear out all tasks
        self.cmdr.stop()

    def test_execer_holds_script_exec_until_task_complete(self):
        script = [('cmd_one', 'now'),
                  ('long_cmd_1', 'relative', 2),
                  ('cmd_two', 'relative', 2),
                  ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.set_debug(True)
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 7
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command long_cmd_1 at 2' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_two at 7' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'long_cmd_1 has finished at 5' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_two has finished at 7' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
