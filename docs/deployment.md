# Production Deployment Guide

This document describes the required steps for deploying the **NutriSys** project into a production environment.

## 1. Hardware Requirements

### Minimum Requirements

| Resource | Requirement                 |
|----------|-----------------------------|
| CPU      | 2 vCPUs                     |
| RAM      | 4 GB                        |
| Storage  | 20 GB SSD                   |
| Network  | Stable broadband connection |

### Recommended Requirements

| Resource | Requirement      |
|----------|------------------|
| CPU      | 4+ vCPUs         |
| RAM      | 8+ GB            |
| Storage  | 80+ GB SSD       |
| GPU      | 1000+ MHz, 1+ GB |

## 2. Required Software

The production server or cluster must have the following software installed:

- Kubernetes Cluster
- kubectl
- Helm
- Git

## 3. Network Configuration

The following network requirements must be satisfied.

### External Access

Allow outbound access to:

- Telegram Bot API
- GitHub Container Registry
- External APIs used by the project

### Internal Cluster Communication

Allow communication between the following components:

| Source         | Destination    | Purpose           |
|----------------|----------------|-------------------|
| Telegram Bot   | Backend Server | API requests      |
| Web Interface  | Backend Server | API requests      |
| Backend Server | MySQL          | Database access   |
| Backend Server | nscale         | Image access/save |

### Security Recommendations

- Expose only required public services (Telegram/ Web-Interface)
- Keep MySQL and Backend end-points internal/private
- Use TLS/HTTPS for public endpoints

## 4. Project Configuration

### Pull latest changes from github

```bash
git clone https://github.com/OxiDis2004/NutriSys.git
cd NutriSys
```

### Create Kubernetes Namespace

```bash
kubectl create namespace stack
```

### Deploy Application

Create config properties

```bash
touch ~/.nutri-system.properties
```

Structure:

    TELEGRAM_BOT_TOKEN=your_telegram_token
    GHCR_USERNAME=your_registry_username
    GHCR_PASSWORD=your_registry_password

Install namespace to cluster

```bash
./local-helm.sh
```

## 5. Verification

#### Verify Pods

```bash
kubectl get pods -n stack
```

#### Verify Deployments

```bash
kubectl get deployments -n stack
```

#### Verify Services

```bash
kubectl get svc -n stack
```

#### Verify Ingress

```bash
kubectl get ing -n stack
```

### Deployment Success Criteria

The production deployment is considered successful when:

- All Kubernetes pods are healthy.
- The backend server is running.
- The Telegram bot responds to user messages.
- The website is at domain available.
- The backend can connect to MySQL.
