FROM python:3.11-slim

ARG APP_USER=stream_voice\
    APP_GROUP=stream_voice\
    CODE_FOLDER=/code


RUN apt update && \
    apt upgrade -y && \
    apt install -y curl


WORKDIR $CODE_FOLDER

RUN groupadd $APP_GROUP && \
    useradd -s /bin/bash -g $APP_GROUP $APP_USER -m && \
    chown -R $APP_USER:$APP_GROUP $CODE_FOLDER

RUN mkdir /venv && chown -R $APP_USER:$APP_GROUP /venv

USER $APP_USER
ENV PATH=${PATH}:/home/$APP_USER/.local/bin \
    PYTHONPATH=${CODE_FOLDER}

RUN pip install -U pip && pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.path /venv && \
    poetry config virtualenvs.in-project false && \
    poetry install


COPY ./stream_voice stream_voice/
COPY ./tests tests/


COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "stream_voice.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--reload-dir", "stream_voice"]
