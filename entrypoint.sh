#!/bin/bash

sleep 5
alembic upgrade head
python3 src/every_day_check.py &
uvicorn src.api:app --host 0.0.0.0 --port 5000