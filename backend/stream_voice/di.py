from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from stream_voice.db import get_async_session
from stream_voice.services import (
    FriendsService,
    MessagerService,
    TunnelTokenService,
    UserService,
)
from stream_voice.ws_channel import Channels


async def get_channels():
    yield Channels()


async def get_user_service(session: AsyncSession = Depends(get_async_session)):
    yield UserService(session=session)


async def get_messager_service(
    channels: Channels = Depends(get_channels),
    session: AsyncSession = Depends(get_async_session),
):
    yield MessagerService(
        channels=channels,
        session=session,
    )


async def get_tunnel_token_service(session: AsyncSession = Depends(get_async_session)):
    yield TunnelTokenService(session=session)


async def get_friends_service(
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
):
    yield FriendsService(session=session, user_service=user_service)
