#!/usr/bin/env bash

mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

exec celery --app=app worker \
            --loglevel=INFO --logfile=/var/log/celery/worker-example.log \
            --statedb=/var/run/celery/worker-example@%h.state \
            --hostname=worker-example@%h \
            --queues=celery.example -O fair \
            --uid=nobody --gid=nogroup