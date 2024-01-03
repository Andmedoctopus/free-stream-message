from sqlalchemy.ext.asyncio import AsyncSession

from stream_voice.models import TunnelToken, User


class TunnelTokenService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_token(self, user: User) -> TunnelToken:
        token = TunnelToken(user=user, active=True)
        self.session.add(token)
        await self.session.commit()

        return token
