from stream_voice.models import User

from .users import PreLoad, UserService

from sqlalchemy.ext.asyncio import AsyncSession

class FriendsService:
    def __init__(self, session: AsyncSession, user_service: UserService):
        self.session = session
        self.user_service = user_service

    async def get_friends(self, username: str):
        user = await self.user_service.get_user(username, PreLoad(friends=True))
        return user.friends

    async def get_friend_requests(self, username: str) -> list[User]:
        user = await self.user_service.get_user(username, PreLoad(friend_requests=True))
        return user.friend_requests

    async def send_request(self, username: str, potential_friend_username: str):
        user = await self.user_service.get_user(
            username, PreLoad(friend_requests=True)
        )
        potential_friend = await self.user_service.get_user(
            potential_friend_username, PreLoad(friend_requests=True)
        )
        if user.id in (user.id for user in potential_friend.friend_requests):
            await self.add_friend(username, potential_friend_username)
            return

        user.friend_requests.append(potential_friend)
        self.session.add(user)
        await self.session.commit()

    async def add_friend(self, username: str, friend_username: str):
        user = await self.user_service.get_user(
            username, PreLoad(friends=True, friend_requests=True)
        )
        friend = await self.user_service.get_user(
            friend_username, PreLoad(friends=True, friend_requests=True)
        )

        try:
            friend.friend_requests.remove(user)
        except ValueError:
            pass

        try:
            user.friend_requests.remove(friend)
        except ValueError:
            pass
        user.friends.append(friend)
        friend.friends.append(user)
        await self.session.commit()
