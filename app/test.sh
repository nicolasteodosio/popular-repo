#!/bin/bash

export TESTING="True"

python3 -m pytest --cov=. --cov-branch --cov-report=term --cov-report=html --cov-config=tests/.coveragerc tests "$1"