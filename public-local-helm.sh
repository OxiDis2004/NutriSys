kubectl create namespace nutri-sys-ns

kubectl create secret generic telegram-secret \
  --from-literal=token=<TELEGRAM-TOKEN> \
  -n nutri-sys-ns

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<GITHUB-USERNAME> \
  --docker-password=<GITHUB-PASSWORD> \
  -n nutri-sys-ns

helm install nutri-sys ./chart -n nutri-sys-ns