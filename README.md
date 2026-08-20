# 🚀 DevOps Orkestrering – JensenStore

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-black?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes\&logoColor=white)](https://kubernetes.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions\&logoColor=white)](https://github.com/features/actions)
[![GHCR](https://img.shields.io/badge/GHCR-Container%20Registry-181717?logo=github\&logoColor=white)](https://github.com/features/packages)
[![Minikube](https://img.shields.io/badge/Minikube-Local%20Kubernetes-94399E?logo=kubernetes\&logoColor=white)](https://minikube.sigs.k8s.io/)

> **A practical DevOps project demonstrating CI/CD, containerization, Kubernetes orchestration, automated testing, self-healing, scaling, rolling deployments, and rollback.**

This project was developed as part of my **IoT & Embedded Systems Development studies at JENSEN yrkeshögskola** and is designed to demonstrate practical skills relevant to a **LIA internship in DevOps, Cloud, IoT, Embedded Linux, or software development**.

---

## 👋 Why This Project Matters

This repository is more than a school exercise. It demonstrates my ability to take an application through a simplified **software delivery lifecycle**:

```text
        DEVELOPMENT
             │
             ▼
       Git / GitHub
             │
             ▼
      Automated Tests
             │
             ▼
       GitHub Actions
             │
             ▼
       Docker Image
             │
             ▼
     GitHub Container
         Registry
             │
             ▼
        Kubernetes
             │
      ┌──────┼──────┐
      ▼      ▼      ▼
    Health  Scale  Recovery
      │
      ▼
 Rolling Update
      │
      ▼
    Rollback
```

The focus is on understanding **how modern development and deployment workflows work together**, rather than simply running individual technologies.

---

# 🎯 Project Objectives

The main objectives were to gain hands-on experience with:

* CI/CD automation
* Automated software testing
* Docker containerization
* Container image versioning
* GitHub Actions
* GitHub Container Registry
* Kubernetes Deployments
* Kubernetes Services
* Replica management
* Self-healing workloads
* Horizontal scaling
* Readiness and liveness probes
* Rolling updates
* Rollback and recovery
* Kubernetes troubleshooting
* Infrastructure configuration using YAML
* Repeatable deployment scripts

---

# 🏗️ Architecture

## End-to-End Architecture

```text
┌─────────────────────┐
│     Developer       │
│                     │
│  Python / Flask     │
│  Git / GitHub       │
└──────────┬──────────┘
           │
           │ git push
           ▼
┌─────────────────────┐
│    GitHub Repo      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│      GitHub Actions         │
│                             │
│  • Install dependencies     │
│  • Run pytest               │
│  • Build Docker image       │
│  • Authenticate with GHCR   │
│  • Push image               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ GitHub Container Registry   │
│                             │
│ jensenstore-api:<sha>       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│            Kubernetes               │
│             Minikube                │
│                                     │
│       ┌─────────────────────┐       │
│       │     Deployment      │       │
│       │     3 replicas      │       │
│       └─────────┬───────────┘       │
│                 │                   │
│       ┌─────────┼─────────┐         │
│       ▼         ▼         ▼         │
│     Pod 1     Pod 2     Pod 3       │
│       │         │         │         │
│       └─────────┼─────────┘         │
│                 ▼                   │
│          Kubernetes Service         │
│              NodePort               │
│                                     │
│     Readiness + Liveness Probes     │
└─────────────────────────────────────┘
```

---

# 📁 Repository Structure

```text
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
```

---

# 🔄 Del 1 – CI/CD

## Flask REST API

The first part contains a lightweight Flask API with two endpoints.

| Method | Endpoint  | Purpose                             |
| ------ | --------- | ----------------------------------- |
| `GET`  | `/`       | Application information and version |
| `GET`  | `/health` | Health check                        |

Example:

```json
{
  "application": "JensenStore API",
  "status": "running",
  "version": "1.0.0"
}
```

Health endpoint:

```json
{
  "status": "healthy"
}
```

---

## 🧪 Automated Testing

The application uses **pytest** for automated verification.

Run locally:

```powershell
py -3.11 -m pytest -q .\del-1
```

Expected result:

```text
2 passed
```

The same test stage is executed automatically by GitHub Actions.

This demonstrates the principle:

> **Build only after the application has passed automated verification.**

---

# 🐳 Docker Containerization

The Flask application is packaged into a Docker image using **Python 3.12 Slim**.

### Build

```powershell
docker build -t jensenstore-api:del-1 .\del-1
```

### Run

```powershell
docker run --rm -p 8001:8000 jensenstore-api:del-1
```

### Test

```powershell
curl.exe http://localhost:8001/
curl.exe http://localhost:8001/health
```

Docker provides a consistent runtime environment between development and deployment.

---

# ⚙️ GitHub Actions CI/CD

Workflow:

```text
.github/workflows/del-1-ci.yml
```

The pipeline performs:

```text
Git Push
   │
   ▼
Checkout
   │
   ▼
Python 3.12
   │
   ▼
Install Dependencies
   │
   ▼
Run pytest
   │
   ├── ❌ Test failure → Stop
   │
   └── ✅ Tests passed
            │
            ▼
       Docker Build
            │
            ▼
       GHCR Login
            │
            ▼
       Push Image
```

The Docker image is tagged using the Git commit SHA:

```text
ghcr.io/<owner>/<repository>/jensenstore-api:<commit-sha>
```

### Why commit-SHA tagging?

Using the commit SHA creates an immutable relationship between:

```text
Git Commit
     ↓
Docker Image
     ↓
Deployment
```

This makes it easier to identify exactly which source version produced a particular container image.

---

# ☸️ Del 2 – Kubernetes

The second part focuses on container orchestration using:

* Kubernetes
* Minikube
* Docker Desktop
* kubectl

The application is deployed as a Kubernetes Deployment with **3 replicas**.

```text
                Deployment
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        Pod 1     Pod 2     Pod 3
```

---

# 🩺 Health Monitoring

The Deployment uses:

### Readiness Probe

Determines whether the application is ready to receive traffic.

### Liveness Probe

Allows Kubernetes to detect an unhealthy application container and restart it.

```text
                 Pod
                  │
          ┌───────┴───────┐
          ▼               ▼
     Readiness         Liveness
       Probe             Probe
          │               │
          ▼               ▼
    Receive traffic    Restart if
                       unhealthy
```

These mechanisms are important in production Kubernetes environments because they help prevent unhealthy workloads from receiving traffic.

---

# 🔁 Self-Healing

One of the key Kubernetes concepts demonstrated is **reconciliation**.

Delete a running Pod:

```powershell
kubectl delete pod <pod-name>
```

Watch the cluster:

```powershell
kubectl get pods -w
```

Kubernetes observes that:

```text
Desired state = 3 Pods
Actual state  = 2 Pods
```

The controller then creates a replacement:

```text
Pod deleted
    │
    ▼
Actual state changes
    │
    ▼
Kubernetes reconciliation
    │
    ▼
Replacement Pod
    │
    ▼
3 Pods restored
```

This demonstrates Kubernetes' self-healing behavior.

---

# 📈 Horizontal Scaling

The application can be scaled without manually creating Pods.

```powershell
kubectl scale deployment jensenstore --replicas=5
```

Verify:

```powershell
kubectl get deployment
kubectl get pods
```

Kubernetes automatically creates the required additional Pods.

---

# 🔄 Rolling Updates

A second application version is provided:

```text
del-2/k8s/deployment-v2.yaml
```

This allows the project to demonstrate a controlled application update.

Check the rollout:

```powershell
kubectl rollout status deployment/jensenstore
```

View deployment history:

```powershell
kubectl rollout history deployment/jensenstore
```

The rolling-update strategy allows Kubernetes to replace application instances progressively rather than removing the entire workload at once.

---

# ↩️ Rollback & Recovery

If a deployment needs to be reverted:

```powershell
kubectl rollout undo deployment/jensenstore
```

Verify:

```powershell
kubectl rollout status deployment/jensenstore
```

View history:

```powershell
kubectl rollout history deployment/jensenstore
```

This demonstrates a practical recovery workflow:

```text
Version 1
   │
   ▼
Version 2
   │
   ▼
Problem detected
   │
   ▼
Rollback
   │
   ▼
Version 1 restored
```

---

# 🛠️ Troubleshooting & Observability

The project also includes practical Kubernetes troubleshooting.

### Application logs

```powershell
kubectl logs <pod-name>
```

### Pod details

```powershell
kubectl describe pod <pod-name>
```

### Deployment details

```powershell
kubectl describe deployment jensenstore
```

### Cluster events

```powershell
kubectl get events --sort-by=.lastTimestamp
```

### Cluster status

```powershell
kubectl get nodes
```

These commands were used to inspect workload state, investigate behavior, and verify Kubernetes operations.

---

# 📜 Deployment Scripts

The project includes reusable shell scripts:

| Script            | Function                      |
| ----------------- | ----------------------------- |
| `build-v1.sh`     | Build application version 1   |
| `build-v2.sh`     | Build application version 2   |
| `deploy.sh`       | Deploy Kubernetes resources   |
| `kill-one-pod.sh` | Demonstrate self-healing      |
| `watch-pods.sh`   | Monitor Pod state             |
| `cleanup.sh`      | Clean up Kubernetes resources |

The scripts make the exercise more reproducible and reduce repetitive manual commands.

---

# 🧰 Technical Highlights

From an engineering perspective, the most important parts of this project are:

### CI/CD

* GitHub Actions workflow automation
* Automated pytest execution
* Automated Docker image build
* GHCR authentication and publishing
* Commit-SHA image tagging

### Containerization

* Dockerfile-based application packaging
* Python Slim base image
* Container networking and port mapping
* Reproducible runtime environment

### Kubernetes

* Declarative YAML configuration
* Deployments
* Replica management
* Services
* NodePort
* Readiness probes
* Liveness probes
* Self-healing
* Horizontal scaling
* Rolling updates
* Rollback

### Operations

* `kubectl` troubleshooting
* Application logs
* Kubernetes events
* Deployment inspection
* Rollout history
* Repeatable shell scripts

---

# 📊 Verification Results

| Area                   | Result                      |
| ---------------------- | --------------------------- |
| Flask API              | ✅ Working                   |
| `/health` endpoint     | ✅ Healthy                   |
| Automated tests        | ✅ 2 passed                  |
| Docker build           | ✅ Successful                |
| Docker container       | ✅ Verified                  |
| GitHub Actions         | ✅ CI/CD pipeline configured |
| GHCR publishing        | ✅ Configured                |
| Kubernetes Deployment  | ✅ Verified                  |
| Replicas               | ✅ 3 replicas                |
| NodePort Service       | ✅ Verified                  |
| Self-healing           | ✅ Demonstrated              |
| Scaling                | ✅ Demonstrated              |
| Readiness probe        | ✅ Configured                |
| Liveness probe         | ✅ Configured                |
| Rolling update         | ✅ Demonstrated              |
| Rollback               | ✅ Demonstrated              |
| Kubernetes events/logs | ✅ Inspected                 |

---

# 💡 DevOps Skills Demonstrated

This project demonstrates practical experience with:

```text
Git
 │
 ├── Version Control
 ├── Branching / Commits
 └── Repository Management
          │
          ▼
GitHub Actions
 │
 ├── CI
 ├── Automated Testing
 └── Docker Build / Publish
          │
          ▼
Docker
 │
 ├── Images
 ├── Containers
 └── Container Networking
          │
          ▼
Kubernetes
 │
 ├── Deployments
 ├── Services
 ├── Replicas
 ├── Health Probes
 ├── Scaling
 ├── Self-Healing
 ├── Rolling Updates
 └── Rollback
```

---

# 🧠 What I Learned

Through this project, I gained practical understanding of how individual DevOps technologies fit together into a larger delivery pipeline.

In particular, I worked with:

* Declarative infrastructure
* Automated software validation
* Container-based application delivery
* Kubernetes desired-state management
* Failure recovery through reconciliation
* Application health monitoring
* Deployment strategies
* Versioned container images
* Operational troubleshooting

The most important lesson was understanding that **Kubernetes is not simply a way to run containers**. It continuously works to maintain the desired application state and provides mechanisms for availability, scaling, health management, and controlled deployment.

---

# 🚀 Possible Next Steps

This project provides a foundation for further development toward production-oriented DevOps and Cloud environments.

Potential improvements include:

* Deploying to a managed Kubernetes service
* Adding Helm charts
* Implementing Kubernetes Secrets
* Adding ConfigMaps
* Introducing Ingress
* Adding Prometheus and Grafana monitoring
* Adding structured application logging
* Adding security scanning to the CI pipeline
* Adding Docker image vulnerability scanning
* Implementing environment-specific deployments
* Adding infrastructure provisioning with Terraform
* Introducing GitOps with Argo CD

---

# 🎓 Relevance to LIA Internship

This project reflects the type of practical skills I want to develop further during my **LIA internship**.

I am particularly interested in opportunities involving:

* DevOps
* Cloud infrastructure
* CI/CD
* Kubernetes
* Docker
* IoT platforms
* Embedded Linux
* Edge computing
* Automation
* Backend/API development
* Infrastructure and deployment

My background in **IoT & Embedded Systems Development** also gives me an interest in connecting software, devices, networking, and cloud infrastructure.

---

# 🧑‍💻 About Me

**Muhammad Jubayer Akanda**

IoT & Embedded Systems Development Student
JENSEN yrkeshögskola, Stockholm

### Technical interests

```text
IoT • Embedded Systems • DevOps • Cloud
Docker • Kubernetes • Linux • CI/CD
Python • C • C++ • MQTT • REST APIs
Git • GitHub • Automation • Edge Computing
```

I am looking for a **LIA internship where I can contribute to real-world engineering projects while continuing to develop my skills in DevOps, IoT, embedded systems, cloud infrastructure, and software development.**

---

# ⭐ Project Summary

**JensenStore demonstrates an end-to-end DevOps workflow:**

```text
     CODE
       │
       ▼
    TEST
       │
       ▼
   CI / CD
       │
       ▼
    DOCKER
       │
       ▼
     GHCR
       │
       ▼
 KUBERNETES
       │
       ├── 3 Replicas
       ├── Health Checks
       ├── Self-Healing
       ├── Scaling
       ├── Rolling Updates
       └── Rollback
```

> **From source code to containerized, tested, and orchestrated workloads.**

---

## 👤 Author

**Muhammad Jubayer Akanda**

**IoT & Embedded Systems Development | DevOps | Cloud | Kubernetes**

📍 Stockholm, Sweden
