#!/bin/bash
cd meerkat_abacus

celery flower -A  meerkat_abacus.pipeline_worker.celery_app.app &

celery -A  meerkat_abacus.pipeline_worker.celery_app.app worker -l info -Q abacus --concurrency 4

