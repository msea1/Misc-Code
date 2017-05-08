import asyncio
import unittest

from cmdseq.sandbox.aio import ACG, TestBox


class TestCommander(unittest.TestCase):
    def setUp(self):
        self.cmdr = TestBox()
        self.acg = ACG(self.cmdr)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        self.loop.create_task(self.acg.run())

    def tearDown(self):
        self.cmdr.running = False
        for task in asyncio.Task.all_tasks():
            task.cancel()
        self.cmdr.stop()
        self.loop.run_until_complete(self.cmdr.script_queue.join())  # clear out all tasks
        self.loop.run_until_complete(self.cmdr.cmd_queue.join())  # clear out all tasks

    def test_load_commands_to_queue(self):
        cmd_list = [('cmd_one', 'now'),
                    ('cmd_two', 'now'),
                    ('cmd_thr', 'now'),
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'packet', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.cmd_queue.join())
        logs_req_to_be_seen = [False] * 7
        for log_rec in mock_log.records:
            if '3 command(s) added via packet' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_two at 0' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_thr at 0' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'cmd_two has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_thr has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_load_script_to_queue(self):
        cmd_list = [('cmd_one', 'now'),
                    ('cmd_two', 'relative', 1),
                    ('cmd_thr', 'absolute', 3),
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 7
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_two at 1' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_thr at 3' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'cmd_two has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_thr has finished at 3' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_with_script_loaded_queue_accepts_ground(self):
        script = [('script_one', 'now'),
                  ('script_two', 'relative', 2),
                  ('script_thr', 'absolute', 4),
                  ]
        cmd_list = [('cmd_one', 'now'),
                    ('cmd_two', 'now')
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.run_until_complete(asyncio.sleep(0.1))
            self.cmdr.get_message({'type': 'packet', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 12
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command script_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command script_two at 2' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command script_thr at 4' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'script_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'script_two has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'script_thr has finished at 4' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            elif '2 command(s) added via packet' in log_rec.msg:
                logs_req_to_be_seen[7] = True
            elif 'running command cmd_one at 1' in log_rec.msg:
                logs_req_to_be_seen[8] = True
            elif 'running command cmd_two at 1' in log_rec.msg:
                logs_req_to_be_seen[9] = True
            elif 'cmd_one has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[10] = True
            elif 'cmd_two has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[11] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_with_script_loaded_queue_accepts_new_script(self):
        script = [('script_one', 'now'),
                  ('script_two', 'relative', 2),
                  ('script_thr', 'absolute', 4),
                  ]
        script_2 = [('script_alp', 'now'),
                    ('script_brv', 'relative', 2),
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.run_until_complete(asyncio.sleep(0.1))
            self.cmdr.get_message({'type': 'script', 'commands': script_2})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
            self.loop.run_until_complete(asyncio.sleep(0.205))
        logs_req_to_be_seen = [False] * 9
        logs_that_shouldnt_appear = [False] * 2
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command script_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'script_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif '1 command(s) removed from queue' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif '2 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'running command script_alp at 1' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'running command script_brv at 3' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            elif 'script_alp has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[7] = True
            elif 'script_brv has finished at 3' in log_rec.msg:
                logs_req_to_be_seen[8] = True

            elif 'running command script_two' in log_rec.msg:
                logs_that_shouldnt_appear[0] = True
            elif 'running command script_thr' in log_rec.msg:
                logs_that_shouldnt_appear[1] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
        print([x for x in logs_that_shouldnt_appear])
        self.assertTrue(all(x is False for x in logs_that_shouldnt_appear))

    def test_with_script_loaded_and_cmd_running_accepts_new_script(self):
        script = [('script_one', 'now'),
                  ('script_two_long_cmd', 'relative', 2),
                  ('script_thr', 'absolute', 4),
                  ]
        script_2 = [('script_alp', 'now'),
                    ('script_brv', 'relative', 2),
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.run_until_complete(asyncio.sleep(0.3))
            self.cmdr.get_message({'type': 'script', 'commands': script_2})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
            self.loop.run_until_complete(asyncio.sleep(0.205))
        logs_req_to_be_seen = [False] * 10
        logs_that_shouldnt_appear = [False] * 1
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command script_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'script_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif '1 command(s) removed from queue' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif '2 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'running command script_alp at 3' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'running command script_brv at 5' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            elif 'script_alp has finished at 3' in log_rec.msg:
                logs_req_to_be_seen[7] = True
            elif 'script_brv has finished at 5' in log_rec.msg:
                logs_req_to_be_seen[8] = True
            elif 'running command script_two_long_cmd at 2' in log_rec.msg:
                logs_req_to_be_seen[9] = True

            elif 'running command script_thr' in log_rec.msg:
                logs_that_shouldnt_appear[1] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
        print([x for x in logs_that_shouldnt_appear])
        self.assertTrue(all(x is False for x in logs_that_shouldnt_appear))

    def test_execer_holds_script_exec_until_task_complete(self):
        script = [('cmd_one', 'now'),
                  ('long_cmd_1', 'relative', 1),
                  ('cmd_two', 'relative', 1),
                  ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 7
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command long_cmd_1 at 1' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_two at 5' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'long_cmd_1 has finished at 4' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_two has finished at 5' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_execer_holds_script_exec_until_task_complete_but_takes_ground(self):
        script = [('cmd_one', 'now'),
                  ('long_cmd_1', 'relative', 1),
                  ('cmd_two', 'relative', 1),
                  ]
        grnd_cmds = [('cmd_a', 'now'),
                     ('cmd_b', 'now')
                     ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': script})
            self.loop.run_until_complete(asyncio.sleep(0.2))
            self.cmdr.get_message({'type': 'packet', 'commands': grnd_cmds})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 11
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_one at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command long_cmd_1 at 1' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_two at 5' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'running command cmd_a at 2' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'running command cmd_b at 2' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_one has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            elif 'long_cmd_1 has finished at 4' in log_rec.msg:
                logs_req_to_be_seen[7] = True
            elif 'cmd_two has finished at 5' in log_rec.msg:
                logs_req_to_be_seen[8] = True
            elif 'cmd_a has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[9] = True
            elif 'cmd_b has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[10] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_of_absolute_timing_execution_out_of_order(self):
        cmd_list = [('cmd_a', 'absolute', 3),
                    ('cmd_b', 'absolute', 2)
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 4
        for log_rec in mock_log.records:
            if '2 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 3' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'cmd_a has finished at 3' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'cmd_b task is in the past and will be skipped' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_of_absolute_timing_execution_in_order(self):
        cmd_list = [('cmd_a', 'absolute', 2),
                    ('cmd_b', 'absolute', 4)
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 5
        for log_rec in mock_log.records:
            if '2 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 2' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_b at 4' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'cmd_a has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_b has finished at 4' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    
    def test_of_successional_timing_execution_no_prior_cmds(self):
        cmd_list = [('cmd_a', 'relative', 1),
                    ('cmd_b', 'relative', 1),
                    ('cmd_c', 'relative', 1)
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 7
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_b at 1' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_c at 2' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_a has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'cmd_b has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_c has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_of_successional_timing_execution_past_prior_cmd(self):
        old_cmd = [('cmd_prime', 'now')]
        cmd_list = [('cmd_a', 'relative', 1),
                    ('cmd_b', 'relative', 1)
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'packet', 'commands': old_cmd})
            self.loop.run_until_complete(asyncio.sleep(0.3))
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 5
        for log_rec in mock_log.records:
            if '1 command(s) added via packet' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 3' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_b at 4' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'cmd_a has finished at 3' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_b has finished at 4' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))

    def test_of_successional_timing_execution_prior_cmd(self):
        cmd_list = [('cmd_prime', 'now'),
                    ('cmd_a', 'relative', 1),
                    ('cmd_b', 'relative', 1)
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 5
        for log_rec in mock_log.records:
            if '3 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 1' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_b at 2' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'cmd_a has finished at 1' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'cmd_b has finished at 2' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    
    def test_of_immediate_timing_execution(self):
        cmd_list = [('cmd_a', 'now'),
                    ('cmd_b', 'now'),
                    ('cmd_c', 'now'),
                    ('cmd_d', 'now'),
                    ('cmd_e', 'now')
                    ]
        with self.assertLogs(level='DEBUG') as mock_log:
            self.cmdr.get_message({'type': 'script', 'commands': cmd_list})
            self.loop.run_until_complete(self.cmdr.script_queue.join())
        logs_req_to_be_seen = [False] * 11
        for log_rec in mock_log.records:
            if '5 command(s) added via script' in log_rec.msg:
                logs_req_to_be_seen[0] = True
            elif 'running command cmd_a at 0' in log_rec.msg:
                logs_req_to_be_seen[1] = True
            elif 'running command cmd_b at 0' in log_rec.msg:
                logs_req_to_be_seen[2] = True
            elif 'running command cmd_c at 0' in log_rec.msg:
                logs_req_to_be_seen[3] = True
            elif 'running command cmd_d at 0' in log_rec.msg:
                logs_req_to_be_seen[4] = True
            elif 'running command cmd_e at 0' in log_rec.msg:
                logs_req_to_be_seen[5] = True
            elif 'cmd_a has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[6] = True
            elif 'cmd_b has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[7] = True
            elif 'cmd_c has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[8] = True
            elif 'cmd_d has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[9] = True
            elif 'cmd_e has finished at 0' in log_rec.msg:
                logs_req_to_be_seen[10] = True
            print(log_rec.msg)
        print([x for x in logs_req_to_be_seen])
        self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    
    # def test_acg_starts_when_no_commands_in_queue(self):
    #     with self.assertLogs(level='DEBUG') as mock_log:
    #         self.loop.run_until_complete(asyncio.sleep(.7))
    #     logs_req_to_be_seen = [False] * 2
    #     for log_rec in mock_log.records:
    #         if 'running command acg_cmd_1 at 5' in log_rec.msg:
    #             logs_req_to_be_seen[0] = True
    #         elif 'acg_cmd_1 has finished at 5' in log_rec.msg:
    #             logs_req_to_be_seen[1] = True
    #         print(log_rec.msg)
    #     print([x for x in logs_req_to_be_seen])
    #     self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    #
    # def test_acg_kicks_in_after_queue_depleted_and_no_other_commands_added(self):
    #     old_cmd = [('cmd_prime', 'now')]
    #     with self.assertLogs(level='DEBUG') as mock_log:
    #         self.cmdr.get_message({'type': 'packet', 'commands': old_cmd})
    #         self.loop.run_until_complete(asyncio.sleep(.7))
    #     logs_req_to_be_seen = [False] * 5
    #     for log_rec in mock_log.records:
    #         if '1 command(s) added via packet' in log_rec.msg:
    #             logs_req_to_be_seen[0] = True
    #         elif 'running command cmd_prime' in log_rec.msg:
    #             logs_req_to_be_seen[1] = True
    #         elif 'running command acg_cmd_1' in log_rec.msg:
    #             logs_req_to_be_seen[2] = True
    #         elif 'cmd_prime has finished at 0' in log_rec.msg:
    #             logs_req_to_be_seen[3] = True
    #         elif 'acg_cmd_1 has finished at 5' in log_rec.msg:
    #             logs_req_to_be_seen[4] = True
    #         print(log_rec.msg)
    #     print([x for x in logs_req_to_be_seen])
    #     self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    #
    # def test_acg_doesnt_start_after_queue_depleted_if_other_commands_added_within_short_time(self):
    #     old_cmd = [('cmd_prime', 'now')]
    #     new_cmd = [('cmd_new', 'now')]
    #     with self.assertLogs(level='DEBUG') as mock_log:
    #         self.cmdr.get_message({'type': 'packet', 'commands': old_cmd})
    #         self.loop.run_until_complete(self.cmdr.cmd_queue.join())
    #         time.sleep(.4)
    #         self.cmdr.get_message({'type': 'packet', 'commands': new_cmd})
    #         self.loop.run_until_complete(asyncio.sleep(.3))
    #     logs_req_to_be_seen = [False] * 5
    #     logs_that_shouldnt_appear = [False] * 2
    #     for log_rec in mock_log.records:
    #         if '1 command(s) added via packet' in log_rec.msg:
    #             logs_req_to_be_seen[0] = True
    #         elif 'running command cmd_prime at 0' in log_rec.msg:
    #             logs_req_to_be_seen[1] = True
    #         elif 'RESP: cmd_prime has finished at 0' in log_rec.msg:
    #             logs_req_to_be_seen[2] = True
    #         elif 'running command cmd_new at 4' in log_rec.msg:
    #             logs_req_to_be_seen[3] = True
    #         elif 'RESP: cmd_new has finished at 4' in log_rec.msg:
    #             logs_req_to_be_seen[4] = True
    #
    #         elif 'running command acg_cmd_1' in log_rec.msg:
    #             logs_that_shouldnt_appear[0] = True
    #         elif 'acg_cmd_1 has finished at' in log_rec.msg:
    #             logs_that_shouldnt_appear[1] = True
    #         print(log_rec.msg)
    #     print([x for x in logs_req_to_be_seen])
    #     self.assertTrue(all(x is True for x in logs_req_to_be_seen))
    #     print([x for x in logs_that_shouldnt_appear])
    #     self.assertTrue(all(x is False for x in logs_that_shouldnt_appear))
    #
    # def test_acg_resets_after_queue_depleted_and_other_commands_added_within_short_time(self):
    #     old_cmd = [('cmd_prime', 'now')]
    #     new_cmd = [('cmd_new', 'now')]
    #     with self.assertLogs(level='DEBUG') as mock_log:
    #         self.cmdr.get_message({'type': 'packet', 'commands': old_cmd})
    #         self.loop.run_until_complete(self.cmdr.cmd_queue.join())
    #         time.sleep(.4)
    #         self.cmdr.get_message({'type': 'packet', 'commands': new_cmd})
    #         self.loop.run_until_complete(asyncio.sleep(.6))
    #     logs_req_to_be_seen = [False] * 7
    #     for log_rec in mock_log.records:
    #         if '1 command(s) added via packet' in log_rec.msg:
    #             logs_req_to_be_seen[0] = True
    #         elif 'running command cmd_prime at 0' in log_rec.msg:
    #             logs_req_to_be_seen[1] = True
    #         elif 'cmd_prime has finished at 0' in log_rec.msg:
    #             logs_req_to_be_seen[2] = True
    #         elif 'running command cmd_new at 4' in log_rec.msg:
    #             logs_req_to_be_seen[3] = True
    #         elif 'cmd_new has finished at 4' in log_rec.msg:
    #             logs_req_to_be_seen[4] = True
    #         elif 'running command acg_cmd_1 at 9' in log_rec.msg:
    #             logs_req_to_be_seen[5] = True
    #         elif 'acg_cmd_1 has finished at 9' in log_rec.msg:
    #             logs_req_to_be_seen[6] = True
    #         print(log_rec.msg)
    #     print([x for x in logs_req_to_be_seen])
    #     self.assertTrue(all(x is True for x in logs_req_to_be_seen))
