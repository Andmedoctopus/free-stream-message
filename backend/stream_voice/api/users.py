from typing import Annotated

from fastapi import APIRouter, Depends, Query

from stream_voice.di import get_user_service
from stream_voice.models import User
from stream_voice.schemas import UserRead
from stream_voice.services import UserService
from stream_voice.users import current_active_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search")
async def search_user(
    name: Annotated[str, Query(min_length=3)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(current_active_user)],
) -> list[UserRead]:
    users = await user_service.search_user(name)
    return [UserRead.model_validate(user) for user in users]
