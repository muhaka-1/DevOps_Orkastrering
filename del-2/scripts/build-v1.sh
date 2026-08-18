#!/usr/bin/env bash
set -e
docker build -t jensenstore-api:v1 ./app
echo "Built jensenstore-api:v1"
