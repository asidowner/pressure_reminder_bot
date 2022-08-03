run:
	poetry run pd-bot

docker-build:
	docker build -t tgpdbot ./

# обезличить
docker-run:
	docker run -d --name tg -v /path/to/dir/where/db:/home/db tgpdbot

lint:
	poetry run flake8 pd_bot