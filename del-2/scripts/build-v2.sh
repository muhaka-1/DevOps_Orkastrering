#!/usr/bin/env bash
set -e
docker build -t jensenstore-api:v2 ./app
echo "Built jensenstore-api:v2"
