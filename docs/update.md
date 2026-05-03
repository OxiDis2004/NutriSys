# Production Update and Maintenance Guide

This document describes the recommended procedure for updating the NutriSys project in a production environment.

## 1. Preparation for Update

Before starting the update process, the release engineer or DevOps specialist must:

- Review the changelog or release notes of the new version.
- Verify whether database schema changes are included in the release.
- Review newly introduced environment variables or configuration parameters.
- Confirm availability of the new container images in the container registry.

## 2. Backup Creation

Before any production update, create backups of all critical data.

### Required Backups

- Full MySQL database backup
- Current Kubernetes Helm values/configuration

Backups must be stored in a secure location and verified before proceeding.

## 3. Compatibility Verification

Before deployment, ensure that the new version is compatible with the current environment.

### Verify Compatibility Of

- Backend server with current database schema
- Telegram bot with backend API contract

## 4. Deploy New Version

### Update Configuration

Pull or checkout the target release version of the project.

### Update Container Images

Ensure new container images are available and accessible in the registry.

### Apply Updated Deployment Configuration

Deploy the new version using the updated Helm chart and production values.

Kubernetes should perform rolling updates automatically where possible.

### Automation

All the steps described above can be executed using the provided deployment script:

```bash
./update.sh
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

