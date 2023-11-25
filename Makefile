fmt:
	isort .
	black .

dev:
	docker image prune --force
	sudo docker build --file Dockerfile-dev --tag laid-out-dev .
	sudo docker compose --file docker-compose-dev.yml up --build

prod:
	docker image prune --force
	sudo docker compose up
