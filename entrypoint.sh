#!/bin/sh

if [ -z "$1" ]; then
  if [ -z "$(ls --ignore=lost+found $DATA_PATH)" ]; then
    echo "Initializing $DATA_PATH..."
    cp -Rv ./files/. $DATA_PATH
  fi
  exec gunicorn app.main:server -b 0.0.0.0:${SERVER_PORT}
else
  echo "$@"
  exec "$@"
fi
