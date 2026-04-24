#!/usr/bin/env bash

set -euo pipefail

export RELEASE=nutri-sys-ns
export NAMESPACE=stack
export GITHUB_USERNAME=$(grep -E '^github_username=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')
export GITHUB_PASSWORD=$(grep -E '^github_password=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')
export TELEGRAM_TOKEN=$(grep -E '^telegram_token=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')

helm uninstall $RELEASE -n $NAMESPACE
kubectl delete pvc mysql-pvc -n $NAMESPACE

kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic telegram-secret \
  --from-literal=token=$TELEGRAM_TOKEN \
  -n $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=$GITHUB_USERNAME \
  --docker-password=$GITHUB_PASSWORD \
  -n $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

helm upgrade -i $RELEASE ./chart \
  --namespace $NAMESPACE \
  --create-namespace
kubectl config set-context --current --namespace=$NAMESPACE
