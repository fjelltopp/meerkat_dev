#!/bin/bash
set -x
cd meerkat_api/api_background/api_background
celery -A celery_app.app beat &

celery -A celery_app.app worker -Q api_background -l info --concurrency 4

