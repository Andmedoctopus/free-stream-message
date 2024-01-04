from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from stream_voice.exception import ChannelGroupNotFound
from stream_voice.models import Message, User
from stream_voice.services.users import PreLoad, UserService
from stream_voice.ws_channel import Channels


class MessagerService:
    def __init__(
        self, channels: Channels, session: AsyncSession, user_service: UserService
    ):
        self.channels = channels
        self.session = session
        self.user_service = user_service

    async def send_message_to_streamer(
        self, streamer_username: str, current_user: User, message: str
    ):
        streamer = await self.user_service.get_user(
            streamer_username, preload=PreLoad(friends=True, tunnel=True)
        )

        if current_user not in streamer.friends:
            raise ValueError("You are not allowed to send messages to this user")

        token = str(streamer.tunnel_token.token)

        try:
            await self.channels.send_to_group(token, {"message": message})
        except ChannelGroupNotFound:
            pass

        self.session.add(
            Message(
                sender_id=current_user.id,
                receiver_id=streamer.id,
                text=message,
            )
        )
        await self.session.commit()

    async def get_user_messages(self, user: User) -> list[Message]:
        qry = (
            select(Message)
            .filter(Message.receiver_id == user.id)
            .options(joinedload(Message.sender))
        )
        res = await self.session.execute(qry)
        return list(res.scalars().all())

    async def get_tunnel_token(self, current_user: User):
        streamer = await self.user_service.get_user(current_user.username)
        return streamer.tunnel_token
