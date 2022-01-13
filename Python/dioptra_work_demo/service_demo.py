import asyncio
import json
import tempfile
from random import randint
from unittest.mock import patch

from aio_pika import DeliveryMode, Message

from dioptra.service import DioptraService
from rabbitmq_utils.constants import RABBIT_MQ_MAX_PRIORITY
from tests_dioptra.demo.mock_work_generator import mimic_pdp_mq_message

"""
Demo covers:
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

Document code, and TESTING.md too
Add unittests to cover same ground as here
"""

exchange_name = 'amq.topic'
work_items = 10
USE_RABBIT_PRIORITY = True  # flip for dumb queue


class ServiceDemo:
    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.seen_image_ids = [0]
        config = {
            'data_store': {'db_path': self.tempdir.name, 'serial_dir': self.tempdir.name, 'use_sqlite': True, 'load_tests': True},
            'rabbitmq': {'pool_size': 1, 'rabbitmq_host': 'localhost', 'routing_key': 'dioptra.request.#'},
        }
        config['data_store']['serial_dir'] = self.tempdir.name
        self.service = DioptraService(config)
        self.app = {}
        with patch('dioptra.service.DioptraService._database_setup'), patch(
                'dioptra.service.DioptraService._register_api'), patch('t1000.skynet.Skynet.install_hooks'):
            self.service.configure(self.app)
        self.config = config
        self.sesh_worker, self.internal_reader, self.prepper, self.dispatcher, self.uploader = self.service.skynet.workers

    async def run(self):
        await self.sesh_worker.handle_initializing()
        await self.sesh_worker.handle_running()
        await self.internal_reader.handle_initializing()
        self.internal_reader.t1000.process_message = self.mock_read_message
        mock_pdp = self.pub_to_dioptra()

        # fake incoming work
        for i in range(work_items):
            msg = mimic_pdp_mq_message(self.tempdir.name, self.seen_image_ids)
            print(f'Created work item {i}: {msg}')
            priority = randint(1, RABBIT_MQ_MAX_PRIORITY)
            await self.mock_send_message(mock_pdp, 'dioptra.request.pdp', msg, priority)

        await asyncio.sleep(1)  # give it a little time

        for i in range(work_items):
            await self.internal_reader.handle_running()
            await asyncio.sleep(1)

    def pub_to_dioptra(self):
        rabbitmq_context = self.sesh_worker.t1000.session.create_context()
        rabbitmq_context.declare_exchange(exchange_name, type='topic', passive=True)
        rabbitmq_context.freeze()
        return rabbitmq_context

    @staticmethod
    async def mock_send_message(rmq_context, route, message, priority):
        body = json.dumps(message).encode()
        message = Message(body=body, delivery_mode=DeliveryMode.PERSISTENT)
        if USE_RABBIT_PRIORITY:
            message.priority = priority
        async with rmq_context.get_exchange(exchange_name) as exchange:
            await exchange.publish(message, route)

    @staticmethod
    async def mock_read_message(message):
        if message is None:
            return
        data = json.loads(message.body.decode())
        print(f"Body: {data}, with priority {message.priority}" if USE_RABBIT_PRIORITY else f"Body: {data}")
        return data


if __name__ == '__main__':
    demo = ServiceDemo()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(demo.run())
    # demo.verify_stuff()
