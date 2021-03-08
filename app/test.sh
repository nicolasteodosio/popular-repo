#!/bin/bash

export TESTING="True"
export GITHUB_API_ACCESS_TOKEN="token"
export GITHUB_API_URL="https://local"
export REDIS_HOST="localhost"
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_KEY_TTL=600

python3 -m pytest --cov=. --cov-branch --cov-report=term --cov-report=html --cov-config=tests/.coveragerc tests "$1"