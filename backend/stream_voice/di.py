from stream_voice.accessors import MessagerAccessor
from stream_voice.db import async_session_maker
from stream_voice.services import MessagerService, TunnelTokenService
from stream_voice.ws_channel import Channels

channels = Channels()
messager_service = MessagerService()

tunnel_token_service = TunnelTokenService(db=async_session_maker)
messager_accessor = MessagerAccessor(
    messager_service=messager_service, channels=channels, db_session=async_session_maker
)


def get_channels():
    return channels


def get_messager_service():
    return messager_service


def get_messager_accessor():
    return messager_accessor
