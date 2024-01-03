from sqlalchemy import Column, ForeignKey, Table, Uuid

from stream_voice.models import Base

friends_table = Table(
    "friends",
    Base.metadata,
    Column("user_id", Uuid, ForeignKey("user.id"), primary_key=True),
    Column("friend_id", Uuid, ForeignKey("user.id"), primary_key=True),
)

want_to_be_friends_table = Table(
    "want_to_be_friends",
    Base.metadata,
    Column("user_id", Uuid, ForeignKey("user.id"), primary_key=True),
    Column("potential_id", Uuid, ForeignKey("user.id"), primary_key=True),
)
