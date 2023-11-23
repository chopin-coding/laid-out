fmt:
	isort .
	black .

docker-build:
	npm run build
	python ./manage.py collectstatic --noinput
	sudo docker build --tag laid_out .
	sudo docker-compose build

docker-run:
	sudo systemctl stop postgresql
	sudo systemctl stop redis
	docker-compose up
