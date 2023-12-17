from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, WebSocketDisconnect
from starlette.websockets import WebSocket
from stream_voice.ws_channel import Channels

from stream_voice.models import User
from stream_voice.db import create_db_and_tables, remove_db
from stream_voice.schemas import UserCreate, UserRead, UserUpdate
from stream_voice.users import auth_backend, current_active_user, fastapi_users
from stream_voice.di import get_channels

from stream_voice.api import message_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(message_router)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}



@app.websocket("/ws/v1/message/streamer/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    channels: Annotated[Channels, Depends(get_channels)],
):
    await channels.connect(websocket)
    channels.add_to_group(token, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        channels.remove_from_group(token, websocket)
