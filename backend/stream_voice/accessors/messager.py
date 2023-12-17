from sqlalchemy import select
from sqlalchemy.orm import joinedload

from stream_voice.models import User, TunnelToken
from stream_voice.services import MessagerService
from stream_voice.ws_channel import Channels


class MessagerAccessor:
    def __init__(self, messager_service: MessagerService, channels: Channels, db_session):
        self.messager_service = messager_service
        self.channels = channels
        self.db_session = db_session

    async def raise_user_or_tunnel_not_exists(self, username: str):
        async with self.db_session() as session:
            qry = select(User).where(User.username == username)
            res = await session.execute(qry)
            user = res.scalars().first()
            if user is None:
                raise ValueError("Wrong streamer username")
            raise ValueError("No tunnel token for this user")

    async def get_user(self, username: str, detached: bool = True):
        async with self.db_session() as session:
            qry = select(User).options(joinedload(User.tunnel_token)).where(User.username == username)
            res = await session.execute(qry)
            streamer = res.scalars().first()
            if streamer is None:
                await self.raise_user_or_tunnel_not_exists(username)
            return streamer


    async def send_message_to_streamer(self, streamer_username: str, current_user: User, message: str):
        streamer = await self.get_user(streamer_username)
        # check if user can send message to streamer
        token = str(streamer.tunnel_token.token)
        await self.channels.send_to_group(token, {"message": message})


    async def get_tunnel_token(self, current_user: User):
        streamer  = await self.get_user(current_user.username)
        return streamer.tunnel_token
