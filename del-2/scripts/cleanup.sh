#!/usr/bin/env bash
kubectl delete -f k8s/service.yaml --ignore-not-found
kubectl delete deployment jensenstore-api --ignore-not-found
