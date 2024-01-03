from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from stream_voice.models import User


@dataclass
class PreLoad:
    tunnel: bool = False
    friends: bool = False
    friend_requests: bool = False


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, username: str, preload: PreLoad | None = None) -> User:
        if preload is None:
            preload = PreLoad()

        qry = select(User).where(User.username == username)

        if preload.tunnel:
            qry = qry.options(joinedload(User.tunnel_token))
        if preload.friends:
            qry = qry.options(joinedload(User.friends))
        if preload.friend_requests:
            qry = qry.options(joinedload(User.friend_requests))

        res = await self.session.execute(qry)
        user = res.scalars().first()
        if user is None:
            raise ValueError(f"User {username} not found")

        return user

    async def search_user(self, name: str) -> list[User]:
        qry = select(User).where(User.username.ilike(f"%{name}%"))
        res = await self.session.execute(qry)
        return res.scalars().all()
