#!/usr/bin/env bash
kubectl get pods -l app=jensenstore-api -w
