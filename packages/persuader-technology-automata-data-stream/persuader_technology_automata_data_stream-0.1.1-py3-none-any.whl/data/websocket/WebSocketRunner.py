import asyncio
import logging

from coreauth.Authenticator import Authenticator

from data.payload.DataPayloadProcessor import DataPayloadProcessor
from data.websocket.DataWebSocket import DataWebSocket


# todo: need to stop web socket via request or SYS_KILL
# todo: need to handle re-connects
class WebSocketRunner:

    def __init__(self, url, payload_processor: DataPayloadProcessor, ping_interval=20, authenticator: Authenticator = None):
        logging.info(f'Websocket runner initialized with URL:{url}')
        self.url = url
        self.authenticator = self.init_authenticator(authenticator)
        self.payload_processor = payload_processor
        self.web_socket = DataWebSocket(url, ping_interval)
        self.loop = asyncio.get_event_loop()

    def init_authenticator(self, authenticator: Authenticator):
        if authenticator is None:
            return None
        authenticator.authenticate()
        if authenticator.should_update_url():
            self.url = authenticator.update_url(self.url)
        return authenticator

    def fetch_single_payload(self):
        return self.loop.run_until_complete(self.__receive_single_payload())

    async def __receive_single_payload(self):
        async with self.web_socket as ws:
            return await ws.receive()

    def receive_data(self):
        logging.info('Websocket runner set to receiving data')
        asyncio.run(self.__receive_data())

    async def __receive_data(self):
        async with self.web_socket as ws:
            async for payload in ws:
                self.payload_processor.process_payload(payload)
