# Bookinfo Application for Workshop

## Example Installation for "dev" environment
- For others environment do the same just change environment. 
- Also please install **nginx-ingress** and **cert-manager** first.

### 1. Create harbor secret
```
kubectl create secret docker-registry harbor-creds-dev \
  --namespace=bookinfo-dev \
  --docker-username="YOUR_USERNAME" \
  --docker-password="YOUR_PASSWORD"
```

### 2. Create mongodb secret
```
kubectl create secret generic mongodb-creds-dev \
  --namespace bookinfo-dev \
  --from-literal=mongodb-root-password="YOUR_ROOT_PASSWORD" \
  --from-literal=mongodb-passwords="YOUR_PASSWORD" \
  --from-literal=db-username="YOUR_USERNAME"
```

### 3. Create mongodb configmap
```
kubectl create configmap mongodb-init-script-dev \
  --from-file=src/ratings/databases/ratings_data.json \
  --from-file=src/ratings/databases/script.sh \
  -n bookinfo-dev
```

### 4. Helm install
```
# Setup ingress
helm install bookinfo-ingress-dev helm-chart/ingress --namespace bookinfo-dev -f helm-chart/ingress/dev-ingress-values.yaml

# Setup mongodb
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install mongodb-dev bitnami/mongodb --namespace bookinfo-dev -f k8s/mongodb-values/dev-mongodb-values.yaml

# Setup productpage service
helm install bookinfo-productpage-dev helm-chart/productpage --namespace bookinfo-dev -f helm-chart/productpage/dev-productpage-values.yaml

# Setup details service
helm install bookinfo-details-dev helm-chart/details --namespace bookinfo-dev -f helm-chart/details/dev-details-values.yaml

# Setup ratings service
helm install bookinfo-ratings-dev helm-chart/ratings --namespace bookinfo-dev -f helm-chart/ratings/dev-ratings-values.yaml

# Setup reviews service
helm install bookinfo-reviews-dev helm-chart/reviews --namespace bookinfo-dev -f helm-chart/reviews/dev-ratings-values.yaml
```