import asyncio
import json
import tempfile
from typing import Dict
from unittest.mock import patch

import aio_pika
from aio_pika import DeliveryMode, Message

from dioptra.service import DioptraService
from dioptra_work.work_item import DioptraWorkItem
from t1000.worker import WorkerState
from tests_dioptra.demo.mock_work_generator import mimic_pdp_mq_message

# ################# DEFINING SOME THINGS ################# #
exchange_name = 'amq.topic'

"""
How to
    Define Workflow
    Split up into Steps
    Save Plugin Report
    Save Step Report
    Save Workflow Report
    Save result


Dispatch Demo cover:
-getting req
-formulating req
-serializing input
-put on priority Q
-pull off Q
-chunk
-dispatch chunk to subprocess
-subprocess works on it, saves results to files
-dispatch watches subprocesses for exit
-dispatch moves results from files --> DB
-puts back on Q
-loops
-finishes and compiles report(s)
-saves
-begins product/multi-proc
"""


def create_payload_from_new_item(new_item: DioptraWorkItem, calibration_dir):
    # below, an example of perhaps how to create for real
    # raw_image_telem = json.loads(new_item.telemetry_path)
    # image_shape = (raw_image_telem['image.numRows'], raw_image_telem['image.numColumns'])
    # image_file = io.open(new_item.image_path, 'rb')
    # image_data = gen2_extract_image_from_pic_buffer(image_file.read(), image_shape,
    #                                                 is_pic_v9=(raw_image_telem.get('pic_version') == 9),
    #                                                 is_global_4=(new_item.spacecraft_id == 104))
    # sidecar = DiMockWorkflowoptraSidecarData.from_data_dicts(new_item.raw_sat_model, raw_image_telem)
    # calibration_data = DioptraCalibrationData.from_sidecar(sidecar, data_directory=calibration_dir)
    # camera_model = create_camera_model(sidecar, 100, MeanElevationProvider())
    # image = GeoImageWithCamera.create_geo_image('gen2_truesense', image_data, camera_model,
    #                                             bit_depth=12, data_quality_mask=calibration_data.data_quality_mask)
    # sensor_data = DioptraSensorData(image, sidecar, calibration_data)
    # payload = DioptraGen2Payload(bobcat_sensor_data=sensor_data)
    # return payload
    pass


class ScalingDemo:
    def __init__(self, temp_dir: str):
        self.tempdir = temp_dir
        self.seen_image_ids = [0]
        config = {
            'data_store': {'db_path': self.tempdir, 'serial_dir': self.tempdir, 'use_sqlite': True, 'load_tests': True},
            'rabbitmq': {'pool_size': 1, 'rabbitmq_host': 'localhost', 'routing_key': 'dioptra.request.#'},
        }
        config['data_store']['serial_dir'] = self.tempdir
        self.service = DioptraService(config)
        self.app = {}
        with patch('dioptra.service.DioptraService._database_setup'), patch(
                'dioptra.service.DioptraService._register_api'), patch('t1000.skynet.Skynet.install_hooks'):
            self.service.configure(self.app)
        self.config = config
        self.sesh_worker, self.internal_reader, self.dispatcher, _ = self.service.skynet.workers

    async def run(self):
        await self.sesh_worker.handle_initializing()
        await self.sesh_worker.handle_running()
        self.sesh_worker.state = WorkerState.RUNNING

        mock_pdp = self.pub_to_dioptra()

        # fake incoming work
        for _ in range(5):
            msg = mimic_pdp_mq_message(self.tempdir, self.seen_image_ids)
            print(f'mock request from PDP put on queue: {msg}')
            await self.mock_send_message(mock_pdp, 'dioptra.request.pdp', msg)

        await self.service.skynet.start()
        await asyncio.sleep(5)  # to run recv and dispatch

        print(f"Dispatcher's active workers: {self.dispatcher.t1000.num_active_workers}")
        for _ in range(self.dispatcher.t1000.num_active_workers):
            priority, (job, ptr) = self.dispatcher.t1000.active_dispatches.get_nowait()
            print(f"Dispatched: WorkItem for image: {job.image_id} is priority {priority}, with handle {ptr}")
            await self.dispatcher.t1000.handle_completed_work_item(job)

        # show from-dioptra publish
        queue = await self.read_from_dioptra()
        seen = 0
        while seen < 5:
            seen = await self.mock_read_message(queue, seen)
            await asyncio.sleep(1)

    def pub_to_dioptra(self):
        rabbitmq_context = self.sesh_worker.t1000.session.create_context()
        rabbitmq_context.declare_exchange(exchange_name, type='topic', passive=True)
        rabbitmq_context.freeze()
        return rabbitmq_context

    @staticmethod
    async def mock_send_message(rmq_context, route, message: Dict):
        body = json.dumps(message).encode()
        message = Message(body=body, delivery_mode=DeliveryMode.PERSISTENT)
        async with rmq_context.get_exchange(exchange_name) as exchange:
            await exchange.publish(message, route)

    @staticmethod
    async def read_from_dioptra():
        # confirmed this reads from expected exchange and route key
        connection = await aio_pika.connect(host='localhost', heartbeat=10, name='rabbit_demo_reader')
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchange_name, type='topic', passive=True)
        queue = await channel.declare_queue(name='demo_read_status')
        await queue.bind(exchange, routing_key='some.key')
        return queue

    @staticmethod
    async def mock_read_message(queue, num_seen):
        # messages come from PDP, API calls, CLI, etc
        message = await queue.get(fail=False)
        if message is None:
            print('nothing getting out')
            return num_seen
        async with message.process(requeue=True):
            message_data = json.loads(message.body.decode())
        print(f"Status update on {message_data}!")
        return num_seen + 1


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as tempdir:
        demo = ScalingDemo(tempdir)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(demo.run())
        # demo.verify_stuff()
