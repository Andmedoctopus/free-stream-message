from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from stream_voice.di import get_messager_service
from stream_voice.models import User
from stream_voice.schemas import UserRead
from stream_voice.services import MessagerService
from stream_voice.users import current_active_user

router = APIRouter(
    prefix="/api/v1/message",
    tags=["message"],
    responses={404: {"description": "Not found"}},
)


class MessageResponse(BaseModel):
    id: int
    text: str
    sender: UserRead
    model_config = ConfigDict(from_attributes=True)


class SendMessageResponse(BaseModel):
    sent: bool = False
    reason: None | str = None


class GetLinkResponse(BaseModel):
    link: str


class PostMessage(BaseModel):
    message: str


@router.post("/send/{streamer_username}")
async def send_message_to_streamer(
    streamer_username: str,
    message: PostMessage,
    current_user: Annotated[User, Depends(current_active_user)],
    messager_service: Annotated[MessagerService, Depends(get_messager_service)],
) -> SendMessageResponse:
    try:
        await messager_service.send_message_to_streamer(
            streamer_username, current_user, message.message
        )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    return SendMessageResponse(sent=True)


@router.get("")
async def get_user_messages(
    current_user: Annotated[User, Depends(current_active_user)],
    messager_service: Annotated[MessagerService, Depends(get_messager_service)],
) -> list[MessageResponse]:
    messages = await messager_service.get_user_messages(current_user)
    return [MessageResponse.model_validate(message) for message in messages]


@router.get("/send-link")
async def get_send_link(
    current_user: Annotated[User, Depends(current_active_user)],
    messager_service: Annotated[MessagerService, Depends(get_messager_service)],
):
    tunnel_token = await messager_service.get_tunnel_token(current_user)
    return {
        "link": f"http://localhost:8000/ws/v1/message/streamer/{tunnel_token.token}"
    }
