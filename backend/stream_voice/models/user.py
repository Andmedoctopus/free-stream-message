from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stream_voice.models import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(30))
    tunnel_token: Mapped["TunnelToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
