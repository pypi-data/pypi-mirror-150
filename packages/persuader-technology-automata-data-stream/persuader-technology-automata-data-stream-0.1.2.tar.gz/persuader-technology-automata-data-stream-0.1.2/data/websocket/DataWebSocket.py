import logging

from websockets import connect


class DataWebSocket:

    def __init__(self, url, ping_interval):
        logging.info(f'Web socket INITIALIZED with url:[{url}]')
        self.url = url
        self.ping_interval = ping_interval

    async def __aenter__(self):
        logging.info(f'Web socket CONNECTING to url:[{self.url}]')
        self._conn = connect(self.url, ping_interval=self.ping_interval)
        self.websocket = await self._conn.__aenter__()

        return self

    async def __aexit__(self, *args, **kwargs):
        logging.info(f'Web socket DISCONNECTING from url:[{self.url}]')
        await self._conn.__aexit__(*args, **kwargs)

    def __aiter__(self):
        return self

    async def __anext__(self):
        payload = await self.receive()
        if payload:
            return payload
        else:
            raise StopAsyncIteration

    async def receive(self):
        return await self.websocket.recv()
