import asyncio
import random
import time

import aiohttp
from dns import resolver


class BaseSyncLocator:
    def __init__(self, scheme, host, port):
        self.scheme = scheme
        self.host = host
        self.port = port

    def get_address(self):
        host, port = self.get_host_and_port()
        return format_address(self.scheme, host, port)


class SrvLocator(BaseSyncLocator):
    def __init__(self, scheme, host, port):
        super().__init__(scheme, host, port)

    def get_host_and_port(self):
        results = resolver.query(self.host, 'SRV')
        result = random.choice(results)
        return result.target.to_text(), result.port


async def receive_loop():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://{host}:{port}/v1/receive'.format(host=host, port=port)) as ws:
            print('I am connected')
            counter = 0
            async for packet in ws:
                try:
                    data = packet.json()
                    packet_counter = data['FrameSeq']
                    if packet_counter - counter != 1:
                        print(time.time(), "WARNING, POSSIBLE MISSED PACKET", packet_counter, counter)

                    counter = packet_counter
                except Exception as e:
                    print(e)
                    pass


router = SrvLocator('http', 'sft-packet-router.service.lke.gemini', None)
host, port = router.get_host_and_port()
asyncio.get_event_loop().run_until_complete(receive_loop())
