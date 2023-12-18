from stream_voice.models import TunnelToken, User


class TunnelTokenService:
    def __init__(self, db):
        self.db = db

    async def generate_token(self, user: User) -> TunnelToken:
        async with self.db() as session:
            user = await session.merge(user)
            token = TunnelToken(user=user)
            session.add(token)
            await session.commit()
        return token
