DevOps Orkestrering – JensenStore

A complete DevOps exercise demonstrating the progression from application development and CI/CD to container orchestration with Kubernetes.

The project combines:

Del 1 – CI/CD: Flask API, automated tests, Docker image creation, and delivery to GitHub Container Registry (GHCR).

Del 2 – Kubernetes: Container deployment, Services, replicas, self-healing, scaling, rolling updates, rollback, and health probes using Minikube.

1. Project Overview

The purpose of this project is to demonstrate a practical DevOps workflow for the JensenStore API:

Developer
   │
   │ git push
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ├── Install dependencies
   ├── Run automated tests
   ├── Build Docker image
   └── Push image to GHCR
            │
            ▼
   GitHub Container Registry
            │
            ▼
       Kubernetes
         (Del 2)
            │
            ├── Deployment
            ├── 3 replicas
            ├── Service / NodePort
            ├── Readiness probe
            ├── Liveness probe
            ├── Self-healing
            ├── Scaling
            ├── Rolling update
            └── Rollback

2. Repository Structure

DevOps_Orkestrering/
│
├── .github/
│   └── workflows/
│       └── del-1-ci.yml
│
├── del-1/
│   ├── .dockerignore
│   ├── app.py
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── test_app.py
│
├── del-2/
│   ├── app/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── deployment-v2.yaml
│   │   └── service.yaml
│   │
│   └── scripts/
│       ├── build-v1.sh
│       ├── build-v2.sh
│       ├── cleanup.sh
│       ├── deploy.sh
│       ├── kill-one-pod.sh
│       └── watch-pods.sh
│
└── README.md

3. Del 1 – CI/CD Pipeline

Application

Del 1 contains a small Flask REST API.

Endpoints

Method

Endpoint

Purpose

GET

/

Returns application information and version

GET

/health

Health check endpoint

Example:

{
  "application": "JensenStore API",
  "status": "running",
  "version": "1.0.0"
}

Health endpoint:

{
  "status": "healthy"
}

Automated Tests

The application contains automated tests using pytest.

Run locally from the repository root:

py -3.11 -m pytest -q .\del-1

Expected result:

2 passed

The CI pipeline performs the same verification automatically.

Docker

The application is containerized using Docker and Python 3.12 Slim.

Build locally:

docker build -t jensenstore-api:del-1 .\del-1

Run the container:

docker run --rm -p 8001:8000 jensenstore-api:del-1

Test the API:

curl.exe http://localhost:8001/
curl.exe http://localhost:8001/health

Expected responses:

{"application":"JensenStore API","status":"running","version":"1.0.0"}

{"status":"healthy"}

GitHub Actions

The CI workflow is located at:

.github/workflows/del-1-ci.yml

The workflow is triggered when changes are pushed to:

del-1/**
.github/workflows/del-1-ci.yml

It can also be started manually with workflow_dispatch.

Pipeline stages

Checkout source code

Set up Python 3.12

Install dependencies

Run pytest

Build the Docker image

Authenticate with GitHub Container Registry

Push the image to GHCR

The image is tagged using the Git commit SHA:

ghcr.io/<owner>/<repository>/jensenstore-api:<commit-sha>

This provides an immutable reference to the exact source version used to build the image.

4. Del 2 – Kubernetes Orchestration

Del 2 demonstrates how the JensenStore API can be deployed and managed with Kubernetes.

The Kubernetes environment used during the exercise is Minikube with Docker Desktop.

Kubernetes Resources

The main Kubernetes manifests are located in:

del-2/k8s/

Deployment

deployment.yaml defines the application Deployment and its desired state.

The exercise uses 3 replicas to demonstrate availability and Kubernetes reconciliation.

Conceptually:

JensenStore Deployment
        │
        ├── Pod 1
        ├── Pod 2
        └── Pod 3

If one Pod is deleted, Kubernetes automatically creates a replacement.

Service

service.yaml exposes the application through a Kubernetes Service.

The exercise uses a NodePort to make the application accessible from outside the Kubernetes cluster.

Example:

Port 80 → NodePort 30080

Health Probes

The Kubernetes deployment includes:

Readiness probe – determines whether a Pod is ready to receive traffic.

Liveness probe – allows Kubernetes to detect an unhealthy container and restart it.

These probes improve reliability and demonstrate production-oriented Kubernetes practices.

5. Kubernetes Operations Demonstrated

The project demonstrates the following Kubernetes concepts.

Desired state

The Deployment declares how many application replicas should exist.

kubectl get deployment

Example:

NAME          READY   UP-TO-DATE   AVAILABLE
jensenstore   3/3     3            3

Pod self-healing

Delete a Pod:

kubectl delete pod <pod-name>

Then observe:

kubectl get pods -w

Kubernetes detects that the actual state differs from the desired state and creates a replacement Pod.

Scaling

The application can be scaled using:

kubectl scale deployment jensenstore --replicas=5

Verify:

kubectl get deployment
kubectl get pods

The number of Pods should converge to the requested replica count.

Rolling update

The project includes a second application version:

del-2/k8s/deployment-v2.yaml

This is used to demonstrate a Kubernetes rolling update.

Check rollout status:

kubectl rollout status deployment/jensenstore

Check rollout history:

kubectl rollout history deployment/jensenstore

Rollback

If a deployment needs to be reverted:

kubectl rollout undo deployment/jensenstore

Verify:

kubectl rollout status deployment/jensenstore

This demonstrates how Kubernetes can safely return to a previous ReplicaSet revision.

6. Useful Kubernetes Commands

Check the cluster:

kubectl get nodes

Check Deployments:

kubectl get deployments

Check Pods:

kubectl get pods

Watch Pods:

kubectl get pods -w

Check Services:

kubectl get services

Inspect a Deployment:

kubectl describe deployment jensenstore

Inspect a Pod:

kubectl describe pod <pod-name>

View application logs:

kubectl logs <pod-name>

Check Kubernetes events:

kubectl get events --sort-by=.lastTimestamp

Check rollout status:

kubectl rollout status deployment/jensenstore

Check rollout history:

kubectl rollout history deployment/jensenstore

7. Build and Deployment Scripts

The del-2/scripts directory contains helper scripts for common operations:

Script

Purpose

build-v1.sh

Build the first application image

build-v2.sh

Build the second application version

deploy.sh

Deploy the Kubernetes resources

kill-one-pod.sh

Delete one Pod to demonstrate self-healing

watch-pods.sh

Monitor Pod state

cleanup.sh

Remove the Kubernetes resources

The scripts support repeatable execution of the Kubernetes exercise.

8. Verification

The project was verified at multiple levels.

Application

GET /
GET /health

Both endpoints return successful responses.

Automated tests

2 passed

Docker

The Del-1 image builds successfully:

jensenstore-api:del-1

The container was successfully started and tested through port 8001.

CI/CD

GitHub Actions successfully performs:

Checkout
   ↓
Python setup
   ↓
Dependency installation
   ↓
Automated tests
   ↓
Docker build
   ↓
GHCR authentication
   ↓
Docker image push

Kubernetes

The Kubernetes deployment was verified with:

3 application replicas

Service exposure through NodePort

Pod deletion and automatic recovery

Scaling

Readiness and liveness probes

Rolling updates

Rollout history

Rollback

Kubernetes events and logs

9. Technologies Used

Technology

Purpose

Python

Application development

Flask

REST API

pytest

Automated testing

Docker

Containerization

Git

Version control

GitHub

Source control and collaboration

GitHub Actions

CI/CD automation

GitHub Container Registry

Container image registry

Kubernetes

Container orchestration

Minikube

Local Kubernetes cluster

Docker Desktop

Container runtime

kubectl

Kubernetes management

10. DevOps Practices Demonstrated

This project demonstrates several core DevOps principles:

Version control with Git and GitHub

Continuous Integration with GitHub Actions

Automated testing

Containerization

Container image versioning

Continuous delivery to GHCR

Infrastructure configuration using Kubernetes YAML

Desired-state management

Self-healing

High availability through replicas

Horizontal scaling

Health monitoring

Rolling deployments

Rollback and recovery

Repeatable deployment scripts

11. Project Outcome

The project demonstrates a complete path from application source code to an orchestrated container workload:

Source Code
    │
    ▼
Automated Tests
    │
    ▼
Docker Image
    │
    ▼
GitHub Container Registry
    │
    ▼
Kubernetes Deployment
    │
    ▼
3 Replicas
    │
    ├── Health Checks
    ├── Self-Healing
    ├── Scaling
    ├── Rolling Update
    └── Rollback

The result is a reproducible DevOps workflow where application changes can be validated automatically, packaged as a container image, stored in a registry, and prepared for Kubernetes-based deployment.

Author

Muhammad Jubayer Akanda

DevOps / IoT & Embedded Systems Development
