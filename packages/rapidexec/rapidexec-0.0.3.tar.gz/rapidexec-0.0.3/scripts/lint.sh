#!/bin/bash -e

APP_PATH="rapidexec"


ruff "$APP_PATH"
black "$APP_PATH" --check