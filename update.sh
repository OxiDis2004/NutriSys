#!/usr/bin/env bash

set -euo pipefail

export RELEASE=nutri-sys-ns
export NAMESPACE=stack
export GITHUB_USERNAME=$(grep -E '^github_username=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')
export GITHUB_PASSWORD=$(grep -E '^github_password=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')
export TELEGRAM_TOKEN=$(grep -E '^telegram_token=' ~/.nutri-system.properties | cut -d= -f2- | tr -d '\r')

helm upgrade "$RELEASE" ./chart --namespace "$NAMESPACE"

kubectl rollout status deployment/server -n "$NAMESPACE"
kubectl rollout status deployment/telegram-bot -n "$NAMESPACE"
kubectl rollout status deployment/web-frontend -n "$NAMESPACE"

kubectl config set-context --current --namespace="$NAMESPACE"