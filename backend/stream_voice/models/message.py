from sqlalchemy import ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stream_voice.models import Base


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[Text] = mapped_column(Text, nullable=False)

    receiver_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("user.id"))
    receiver: Mapped["User"] = relationship(
        back_populates="messages", foreign_keys=[receiver_id]
    )

    sender_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("user.id"))
    sender: Mapped["User"] = relationship(
        back_populates="messages_sent", foreign_keys=[sender_id]
    )
