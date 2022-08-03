# Pressure reminder bot

This bot can save pressure data, visualizes data and remind save pressure data

### Env params
PD_BOT_TOKEN - telegram bot token
PD_BOT_ALLOWED_CHAT_ID - allowed chat id (only one)

if use docker edit Dockerfile

### Config

path: pd_bot/config.py

* DB_PATH -> path to db where create db (directory where file will be place should be created before start)

* PLOT_DIR_NAME -> path to save plot files (directory where file will be place should be created before start)


### For run by docker:

```
docker build -t tgpdbot ./
docker run -d --name tg -v /path/to/dir/where/db/db:/home/db tgpdbot
```

### For run locally

```
poetry run pd-bot
```
