#!/usr/bin/env bash
set -e

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods

context=$(kubectl config current-context)

echo
echo "Deployment created in context: $context"

if [[ "$context" == "minikube" ]]; then
  echo "Run this command and keep its terminal open:"
  echo "minikube service jensenstore-api --url"
else
  echo "For Docker Desktop Kubernetes, open:"
  echo "http://localhost:30080"
  echo
  echo "If that address does not work, see del-2/README.md for alternatives."
fi
