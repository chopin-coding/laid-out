<h1 align="center">Welcome to Laid Out 🖤</h1>

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<p>
  <a href="https://github.com/chopin-coding/laid-out/blob/main/LICENSE" target="_blank">
    <img alt="License: AGPL 3.0" src="https://img.shields.io/badge/License-AGPL 3.0-yellow.svg" />
  </a>
</p>

> A self-help web app with minimalistic tools.

## Local Development

### Overview

- Local development happens via docker-compose
- Django and django-rest-framework backend; the backend and frontend aren't fully decoupled, only three pages (Anxiety,
  Gratitude, and Journal use Vue.js SFCs)
- Postgres as the DB
- Celery worker for tasks and Celery Beat for task scheduling
- [Flower](https://flower.readthedocs.io/en/latest/) for Celery monitoring/management
- Redis as a message broker for Celery
- Vite dev server (HMR client) for Typescript, Tailwind, and Vue.js SFCs (all pre-compiled and statically served in
  prod)
- [Mailpit](https://github.com/axllent/mailpit) for local email testing

### Getting Started With Local Development

- Install docker and
  docker-compose ([helpful blog](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04))


- Create an empty .allauth file

```sh
touch .envs/.local/.allauth
```

- Install pre-commit

https://pre-commit.com/#install

- Once pre-commit is installed, run

```sh
pre-commit install
```

- Start the development environment

```sh
docker compose --file local.yml up --build -d
```

Django: http://localhost:8000 <br>
Flower: http://localhost:5555 <br>
Mailpit: http://localhost:8025

### Running Tests

```sh
docker compose --file local.yml run --rm django pytest
```

For extra information,
  visit [cookiecutter-django documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html).

## 🤝 Contributing

Contributions, issues, feature requests, and pixel pets are welcome! <br>
Feel free to check the [issues page](https://github.com/chopin-coding/laid-out/issues).

## 📝 License

Copyright © 2024 [Emre Erguvan](https://github.com/chopin-coding).<br />
This project is [AGPL 3.0](https://github.com/chopin-coding/laid-out/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
