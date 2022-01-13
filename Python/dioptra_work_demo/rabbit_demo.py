import asyncio
import json
from random import randint
from unittest.mock import patch

from aio_pika import DeliveryMode, Message

from dioptra.service import DioptraService
from rabbitmq_utils.constants import RABBIT_MQ_MAX_PRIORITY

exchange_name = "amq.topic"
work_items = 5

"""
To Run: First, build and run the rabbitmq docker. Then, you can simply run the rabbit_demo.py script in
the `tests_dioptra` folder. Observe messages pass to and fro from there.

Example stdout w/o priority
Body: work item 1
Body: work item 2
Body: work item 3
Body: work item 4
Body: work item 5
Process finished with exit code 0

w/priority
Body: work item 1, with priority 8
Body: work item 5, with priority 6
Body: work item 2, with priority 5
Body: work item 3, with priority 5
Body: work item 4, with priority 1
Process finished with exit code 0
"""

USE_RABBIT_PRIORITY = True  # flip for dumb queue


class RabbitDemo:
    def __init__(self):
        config = {
            'data_store': {'db_path': 'tmp/rabbit_demo', 'serial_dir': 'tmp/rabbit_demo', 'use_sqlite': True, 'load_tests': True},
            'rabbitmq': {'pool_size': 1, 'rabbitmq_host': 'localhost', 'routing_key': 'dioptra.request.#'},
        }
        self.service = DioptraService(config)
        self.app = {}
        with patch('dioptra.service.DioptraService._database_setup'), patch(
                'dioptra.service.DioptraService._register_api'), patch('t1000.skynet.Skynet.install_hooks'):
            self.service.configure(self.app)
        self.config = config
        self.sesh_worker, self.internal_reader, _, _, _ = self.service.skynet.workers

    async def run(self):
        await self.sesh_worker.handle_initializing()
        await self.sesh_worker.handle_running()

        # aio_pika method
        # connection = await aio_pika.connect(host='localhost', heartbeat=10, name='rabbit_demo_reader')
        # channel = await connection.channel()
        # exchange = await channel.declare_exchange(exchange_name, type='topic', passive=True)
        # queue = await channel.declare_queue(exclusive=True)
        # await queue.bind(exchange, routing_key=routing_key)

        # rabbit_utils wrapper method
        await self.internal_reader.handle_initializing()
        self.internal_reader.t1000.process_message = self.mock_read_message
        self.internal_reader.t1000.organize_work_item = self.pass_fx

        mock_pdp = self.pub_to_dioptra()

        # fake incoming work
        for i in range(work_items):
            msg = f"work item {i + 1}"
            priority = randint(1, RABBIT_MQ_MAX_PRIORITY)
            await self.mock_send_message(mock_pdp, 'dioptra.request.pdp', msg, priority)

        await asyncio.sleep(5)  # give it a little time

        # read from queue, should be in priority
        for i in range(work_items):
            await self.internal_reader.handle_running()

    def pub_to_dioptra(self):
        # aio_pika method
        # connection = await aio_pika.connect(host='localhost', heartbeat=10, name='rabbit_demo_writer')
        # channel = await connection.channel()
        # return await channel.declare_exchange(self.config['rabbitmq_inbound']['exchange_name'], type='topic', passive=True)

        # rabbit_utils wrapper method
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
    def mock_read_message(message):
        if message is None:
            return
        data = json.loads(message.body.decode())
        print(f"Body: {data}, with priority {message.priority}" if USE_RABBIT_PRIORITY else f"Body: {data}")
        return data

    @staticmethod
    def pass_fx(*args):
        pass


if __name__ == '__main__':
    demo = RabbitDemo()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(demo.run())
