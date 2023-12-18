from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from stream_voice.accessors.messager import MessagerAccessor
from stream_voice.di import get_messager_accessor
from stream_voice.models import User
from stream_voice.users import current_active_user

router = APIRouter(
    prefix="/api/v1/message",
    tags=["message"],
    responses={404: {"description": "Not found"}},
)


class MessageResponse(BaseModel):
    sent: bool = False


class GetLinkResponse(BaseModel):
    link: str


class PostMessage(BaseModel):
    message: str


@router.post("/send/{streamer_username}")
async def send_message_to_streamer(
    streamer_username: str,
    message: PostMessage,
    current_user: Annotated[User, Depends(current_active_user)],
    messager_accessor: Annotated[MessagerAccessor, Depends(get_messager_accessor)],
) -> MessageResponse:
    await messager_accessor.send_message_to_streamer(
        streamer_username, current_user, message.message
    )
    return MessageResponse(sent=True)


@router.get("/send-link")
async def get_send_link(
    current_user: Annotated[User, Depends(current_active_user)],
    messager_accessor: Annotated[MessagerAccessor, Depends(get_messager_accessor)],
):
    tunnel_token = await messager_accessor.get_tunnel_token(current_user)
    return {
        "link": f"http://localhost:8000/ws/v1/message/streamer/{tunnel_token.token}"
    }
