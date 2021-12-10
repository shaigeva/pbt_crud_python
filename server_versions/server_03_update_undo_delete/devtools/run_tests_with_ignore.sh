#!/usr/bin/env bash
set -e
set -x

pipenv run pytest --ignore=tests/test_sample.py
