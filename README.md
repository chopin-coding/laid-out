<h1 align="center">Welcome to Laid Out 👋</h1>

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<p>
  <a href="https://github.com/chopin-coding/laid-out/blob/main/LICENSE" target="_blank">
    <img alt="License: AGPL 3.0" src="https://img.shields.io/badge/License-AGPL 3.0-yellow.svg" />
  </a>
</p>

> A self-help web app.

## Install Instructions for Linux

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

Django: http://localhost:8000

Flower: http://localhost:5555

Mailpit: http://localhost:8025

## Run Tests

```sh
docker compose --file local.yml run --rm django pytest
```

- For extra information
  visit [cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to
check [issues page](https://github.com/chopin-coding/laid-out/issues).

## 📝 License

Copyright © 2024 [Emre Erguvan](https://github.com/chopin-coding).<br />
This project is [AGPL 3.0](https://github.com/chopin-coding/laid-out/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
