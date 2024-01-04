class ChannelGroupNotFound(KeyError):
    def __init__(self, group: str):
        message = f"No such group ({group})"
        super().__init__(message)
