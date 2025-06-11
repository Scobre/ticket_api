#!/bin/sh

case "$FASTAPI_ENV" in
  production|preproduction)
    echo "Run fastapi in production mode"
    fastapi run main.py --host 0.0.0.0 --port 8000
    ;;
  *)
    echo "Run fastapi in development mode"
    fastapi dev main.py --host 0.0.0.0 --port 8000
    ;;
esac
