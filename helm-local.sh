kubectl create namespace nutri-sys-ns

kubectl create secret docker-registry ghrc-secret \
  --docker-server=ghcr.io \
  --docker-username=OxiDis2004 \
  --docker-password= \
  -n nutri-sys-ns

helm install nutri-sys ./chart -n nutri-sys-ns