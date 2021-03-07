#!/bin/bash

export TESTING="True"
export GITHUB_API_ACCESS_TOKEN="token"
export GITHUB_API_URL="https://local"

python3 -m pytest --cov=. --cov-branch --cov-report=term --cov-report=html --cov-config=tests/.coveragerc tests "$1"