import uuid
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from stream_voice.models import Base


class TunnelToken(Base):
    __tablename__ = "tunnel_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, default=uuid.uuid4)
    active: Mapped[bool] = mapped_column(nullable=False, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tunnel_token")
