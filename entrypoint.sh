#!/bin/bash
APP_PORT=${PORT:-8000}
cd /usr/src/app/
/opt/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}