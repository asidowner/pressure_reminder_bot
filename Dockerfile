FROM python:3.10

WORKDIR /home

# обезличить
ENV PD_BOT_TOKEN=''
# обезличить
ENV PD_BOT_ALLOWED_CHAT_ID=''

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip poetry && apt-get update && apt-get install sqlite3
ADD pd_bot ./pd_bot
ADD plots ./plots
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry env use python && poetry install


CMD poetry run pd-bot