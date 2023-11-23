FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /django

COPY ./requirements.txt /django
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000