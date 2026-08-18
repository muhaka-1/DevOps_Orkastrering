#!/usr/bin/env bash
set -e
POD=$(kubectl get pods -l app=jensenstore-api -o jsonpath='{.items[0].metadata.name}')
echo "Deleting pod: $POD"
kubectl delete pod "$POD"
