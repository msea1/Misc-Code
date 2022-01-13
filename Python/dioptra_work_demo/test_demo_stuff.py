import tempfile
import unittest

from dioptra_work.work_item import DioptraWorkItem
from tests_dioptra.demo.mock_work_generator import mimic_pdp_mq_message


class DemoTests(unittest.TestCase):
    def test_mimic_pdp_produces_incoming_item(self):
        with tempfile.TemporaryDirectory() as tempdir:
            msg = mimic_pdp_mq_message(tempdir, [0])
            msg['request_id'] = msg['mission_plan']['request_id']
            msg['task_id'] = msg['mission_plan']['task_id']
            msg['priority'] = msg['mission_plan']['priority']
            job_request = DioptraWorkItem(**msg)
            self.assertTrue(job_request.task_id == msg['mission_plan']['task_id'])

# copied over from previous MR, preserving it in case we find it repurposeful
# class WorkflowStepInstanceTests(unittest.TestCase):
#     def setUp(self):
#         self.start_time = pendulum.parse('1974-04-19T00:00:00+00:00')
#         self.end_time = self.start_time.add(seconds=10)
#
#     def test_run(self):
#         step_instance = WorkflowStepInstance('run_id', DEMO_WORKFLOW.steps[0], 1, self.start_time)
#         payload_in = DioptraPayload()
#         step_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_step_params(dioptra_step, force_insert):
#             step_params.append(dioptra_step.to_dict())
#         plugin_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_plugin_params(demo_plugin_data_model, force_insert):
#             plugin_params.append(demo_plugin_data_model.to_dict())
#
#         with mock.patch('pendulum.DateTime.utcnow', return_value=self.end_time), \
#              mock.patch('dioptra_work.database.models.DioptraStep.save', save_step_params), \
#              mock.patch('tests_dioptra_work.test_plugins.demo_plugin.DemoPluginDataModel.save', save_plugin_params), \
#              self.assertLogs() as logs:
#             payload_out = step_instance.run(payload_in)
#
#         expected_step_params = {
#             "run_id": 'run_id',
#             "step_number": 1,
#             "step_name": 'demo_step_name_1',
#             "plugin_name": 'demo',
#             "plugin_version": 0.1,
#             "plugin_arguments": {},
#             "plugin_diagnostics": {'demo_field_1': 'testing', 'demo_field_2': 'yes, another'},
#             "exit_code": 0,
#             "exit_status": 'success',
#             "execution_time_sec": 10.0,
#             "debug_s3_locations": {},
#         }
#         expected_plugin_params = {
#             "run_id": 'run_id',
#             "step_number": 1,
#             'demo_field_1': 'testing',
#             'demo_field_2': 'yes, another'
#         }
#
#         self.assertIs(payload_out, payload_in)
#         self.assertEqual(step_params[0], expected_step_params)
#         check_logs(logs, f"generating dioptra step report using {expected_step_params}")
#         self.assertEqual(plugin_params[0], expected_plugin_params)
#         check_logs(logs, f"generating demo step report using {expected_plugin_params}")
#
#     def test_run_no_db(self):
#         step_instance = WorkflowStepInstance('run_id', DEMO_WORKFLOW.steps[0], 1, self.start_time, use_db=False)
#         payload_in = DioptraPayload()
#
#         with mock.patch('pendulum.DateTime.utcnow', return_value=self.end_time), \
#              mock.patch('dioptra_work.database.models.DioptraStep.save') as save_step_params, \
#                 mock.patch('tests_dioptra_work.test_plugins.demo_plugin.DemoPluginDataModel.save') as save_plugin_params, \
#                 self.assertLogs() as logs:
#             payload_out = step_instance.run(payload_in)
#
#         expected_step_params = {
#             "run_id": 'run_id',
#             "step_number": 1,
#             "step_name": 'demo_step_name_1',
#             "plugin_name": 'demo',
#             "plugin_version": 0.1,
#             "plugin_arguments": {},
#             "plugin_diagnostics": {'demo_field_1': 'testing', 'demo_field_2': 'yes, another'},
#             "exit_code": 0,
#             "exit_status": 'success',
#             "execution_time_sec": 10.0,
#             "debug_s3_locations": {},
#         }
#         expected_plugin_params = {
#             "run_id": 'run_id',
#             "step_number": 1,
#             'demo_field_1': 'testing',
#             'demo_field_2': 'yes, another'
#         }
#
#         self.assertIs(payload_out, payload_in)
#         save_step_params.assert_not_called()
#         check_logs(logs, f"generating dioptra step report using {expected_step_params}")
#         save_plugin_params.assert_not_called()
#         check_logs(logs, f"generating demo step report using {expected_plugin_params}")
#
#     def test_run_plugin_exception(self):
#         step_instance = WorkflowStepInstance('run_id', FAIL_WORKFLOW.steps[1], 2, self.start_time)
#         payload_in = DioptraPayload()
#         step_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_step_params(dioptra_step, force_insert):
#             step_params.append(dioptra_step.to_dict())
#         plugin_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_plugin_params(demo_plugin_data_model, force_insert):
#             plugin_params.append(demo_plugin_data_model.to_dict())
#
#         with mock.patch('pendulum.DateTime.utcnow', return_value=self.end_time), \
#              mock.patch('dioptra_work.database.models.DioptraStep.save', save_step_params), \
#              mock.patch('tests_dioptra_work.test_plugins.demo_plugin.DemoPluginDataModel.save', save_plugin_params), \
#              self.assertLogs() as logs, \
#                 self.assertRaises(DioptraWorkflowStepFailure):
#             payload_out = step_instance.run(payload_in)
#
#         expected_step_params = {
#             "run_id": 'run_id',
#             "step_number": 2,
#             "step_name": 'fail_step_name_2',
#             "plugin_name": 'demo',
#             "plugin_version": 0.1,
#             "plugin_arguments": FAIL_WORKFLOW.steps[1].arguments,
#             "plugin_diagnostics": {},
#             "exit_code": 3001,
#             "exit_status": 'injected error',
#             "execution_time_sec": 10.0,
#             "debug_s3_locations": {},
#         }
#
#         check_logs(logs, 'Received a obscura plugin exception with error code 3001 while running plugin demo')
#         self.assertEqual(step_params[0], expected_step_params)
#         check_logs(logs, f"generating dioptra step report using {expected_step_params}")
#         self.assertEqual(len(plugin_params), 0)
#         check_unexpected_logs(logs, f"generating demo step report using")
#
#     def test_run_plugin_exception_retry(self):
#         step_instance = WorkflowStepInstance('run_id', FAIL_WORKFLOW.steps[2], 3, self.start_time)
#         payload_in = DioptraPayload()
#         step_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_step_params(dioptra_step, force_insert):
#             step_params.append(dioptra_step.to_dict())
#         plugin_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_plugin_params(demo_plugin_data_model, force_insert):
#             plugin_params.append(demo_plugin_data_model.to_dict())
#
#         with mock.patch('pendulum.DateTime.utcnow', return_value=self.end_time), \
#              mock.patch('dioptra_work.database.models.DioptraStep.save', save_step_params), \
#              mock.patch('tests_dioptra_work.test_plugins.demo_plugin.DemoPluginDataModel.save', save_plugin_params), \
#              self.assertLogs() as logs, \
#                 self.assertRaises(DioptraWorkflowStepRetryableFailure):
#             payload_out = step_instance.run(payload_in)
#
#         expected_step_params = {
#             "run_id": 'run_id',
#             "step_number": 3,
#             "step_name": 'fail_step_name_3',
#             "plugin_name": 'demo',
#             "plugin_version": 0.1,
#             "plugin_arguments": FAIL_WORKFLOW.steps[2].arguments,
#             "plugin_diagnostics": {},
#             "exit_code": 3000,
#             "exit_status": 'injected error',
#             "execution_time_sec": 10.0,
#             "debug_s3_locations": {},
#         }
#
#         check_logs(logs, 'Received a obscura plugin exception with error code 3000 while running plugin demo')
#         self.assertEqual(step_params[0], expected_step_params)
#         check_logs(logs, f"generating dioptra step report using {expected_step_params}")
#         self.assertEqual(len(plugin_params), 0)
#         check_unexpected_logs(logs, f"generating demo step report using")
#
#     def test_run_non_plugin_exception(self):
#         step_instance = WorkflowStepInstance('run_id', FAIL_WORKFLOW.steps[3], 4, self.start_time)
#         payload_in = DioptraPayload()
#         step_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_step_params(dioptra_step, force_insert):
#             step_params.append(dioptra_step.to_dict())
#         plugin_params = []  # Need to modify an existing mutable object for this patch to work.
#         def save_plugin_params(demo_plugin_data_model, force_insert):
#             plugin_params.append(demo_plugin_data_model.to_dict())
#
#         with mock.patch('pendulum.DateTime.utcnow', return_value=self.end_time), \
#              mock.patch('dioptra_work.database.models.DioptraStep.save', save_step_params), \
#              mock.patch('tests_dioptra_work.test_plugins.demo_plugin.DemoPluginDataModel.save', save_plugin_params), \
#              self.assertLogs() as logs, \
#                 self.assertRaises(DioptraWorkflowStepFailure):
#             payload_out = step_instance.run(payload_in)
#
#         expected_step_params = {
#             "run_id": 'run_id',
#             "step_number": 4,
#             "step_name": 'fail_step_name_4',
#             "plugin_name": 'demo',
#             "plugin_version": 0.1,
#             "plugin_arguments": FAIL_WORKFLOW.steps[3].arguments,
#             "plugin_diagnostics": {},
#             "exit_code": -1,
#             "exit_status": 'failed due to injected error',
#             "execution_time_sec": 10.0,
#             "debug_s3_locations": {},
#         }
#
#         check_logs(logs, f"Received unknown exception: injected error while running plugin demo")
#         self.assertEqual(step_params[0], expected_step_params)
#         check_logs(logs, f"generating dioptra step report using {expected_step_params}")
#         self.assertEqual(len(plugin_params), 0)
#         check_unexpected_logs(logs, f"generating demo step report using")
