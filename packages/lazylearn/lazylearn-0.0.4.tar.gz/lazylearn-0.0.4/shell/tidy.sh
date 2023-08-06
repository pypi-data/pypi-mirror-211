#!/bin/bash
#
# Perform code style checks of the Python code.

export PIPENV_VERBOSITY=-1
set -e

echo "--- black ---"
pipenv run black --line-length 88 python/src/lazylearn/
pipenv run black --line-length 88 python/src/test/
echo "--- isort ---"
pipenv run isort python/src/lazylearn/ --multi-line 3 --profile black
pipenv run isort python/src/test/ --multi-line 3 --profile black
