from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from stream_voice.di import get_friends_service
from stream_voice.models import User
from stream_voice.schemas import UserRead
from stream_voice.services import FriendsService
from stream_voice.users import current_active_user

router = APIRouter(
    prefix="/api/v1/friends",
    tags=["friends"],
    responses={404: {"description": "Not found"}},
)


class AddFriendResponse(BaseModel):
    added: bool


@router.post("/send-request/{username}")
async def send_request(
    username: str,
    current_user: Annotated[User, Depends(current_active_user)],
    friend_service: Annotated[FriendsService, Depends(get_friends_service)],
) -> AddFriendResponse:
    await friend_service.send_request(username, current_user.username)
    return AddFriendResponse(added=True)


@router.get("/requests")
async def get_friend_requests(
    current_user: Annotated[User, Depends(current_active_user)],
    friend_service: Annotated[FriendsService, Depends(get_friends_service)],
) -> list[UserRead]:
    potential_friends = await friend_service.get_friend_requests(current_user.username)
    return [
        UserRead.model_validate(potential_friend)
        for potential_friend in potential_friends
    ]


@router.get("/friends")
async def get_friends(
    current_user: Annotated[User, Depends(current_active_user)],
    friend_service: Annotated[FriendsService, Depends(get_friends_service)],
) -> list[UserRead]:
    friends = await friend_service.get_friends(current_user.username)
    return [UserRead.model_validate(friend) for friend in friends]
