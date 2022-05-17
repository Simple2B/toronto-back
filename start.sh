#!/bin/bash
# poetry run inv update
poetry run uvicorn --port 5000 --host 0.0.0.0 --workers 2 app.main:app
