from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stream_voice.models.base import Base
from stream_voice.models.friends import friends_table, want_to_be_friends_table


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(30))
    tunnel_token: Mapped["TunnelToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    friends: Mapped[list["User"]] = relationship(
        "User",
        secondary=friends_table,
        primaryjoin=lambda: friends_table.c.user_id == User.id,
        secondaryjoin=lambda: friends_table.c.friend_id == User.id,
        back_populates="friends",
    )
    friend_requests: Mapped[list["User"]] = relationship(
        "User",
        secondary=want_to_be_friends_table,
        primaryjoin=lambda: want_to_be_friends_table.c.user_id == User.id,
        secondaryjoin=lambda: want_to_be_friends_table.c.potential_id == User.id,
        back_populates="friend_requests",
    )
