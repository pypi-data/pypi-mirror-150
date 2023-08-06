import asyncio

from coreauth.Authenticator import Authenticator

from data.payload.DataPayloadProcessor import DataPayloadProcessor
from data.websocket.DataWebSocket import DataWebSocket


class WebSocketRunner:

    def __init__(self, url, payload_processor: DataPayloadProcessor, ping_interval=20, authenticator: Authenticator = None):
        self.url = url
        self.payload_processor = payload_processor
        self.web_socket = DataWebSocket(self.url, ping_interval, authenticator)
        self.loop = asyncio.get_event_loop()

    def fetch_single_payload(self):
        return self.loop.run_until_complete(self.__receive_single_payload())

    async def __receive_single_payload(self):
        async with self.web_socket as ws:
            return await ws.receive()

    def receive_data(self):
        asyncio.run(self.__receive_data())

    async def __receive_data(self):
        async with self.web_socket as ws:
            async for payload in ws:
                self.payload_processor.process_payload(payload)
