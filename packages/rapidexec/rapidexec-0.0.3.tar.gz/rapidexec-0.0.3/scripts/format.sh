#!/bin/bash -e

APP_PATH="rapidexec"

ruff "$APP_PATH" --fix
black "$APP_PATH"