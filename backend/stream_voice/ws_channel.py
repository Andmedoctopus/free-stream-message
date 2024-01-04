from collections import defaultdict

from starlette.websockets import WebSocket

from stream_voice.exception import ChannelGroupNotFound


class Channels:
    def __init__(self) -> None:
        self.groups: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, client: WebSocket):
        await client.accept()

    async def send_to_group(self, group: str, msg: dict):
        if group not in self.groups:
            raise ChannelGroupNotFound(group)

        for client in self.groups[group]:
            await client.send_json(msg)

    def add_to_group(self, group: str, client: WebSocket):
        self.groups[group].add(client)

    def remove_from_group(self, group: str, client: WebSocket):
        self.groups[group].remove(client)
