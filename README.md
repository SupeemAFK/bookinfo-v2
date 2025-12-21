# Bookinfo Application for Workshop

## Example Installation for "dev" environment
- For others environment do the same just change environment. 
- Also please install **nginx-ingress** and **cert-manager** first.

### 1. Create harbor secret
```
kubectl create secret docker-registry harbor-creds-dev \
  --namespace=bookinfo-dev
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

### 3. Helm install
```
# Setup ingress
helm install bookinfo-ingress-dev helm-chart/ingress --namespace bookinfo-dev -f helm-chart/ingress/ingress-dev-values.yaml

# Setup mongodb
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install mongodb-dev bitnami/mongodb --namespace bookinfo-dev -f k8s/mongodb-values/mongodb-dev-values.yaml

# Setup productpage service
helm install bookinfo-productpage-dev helm-chart/productpage --namespace bookinfo-dev -f helm-chart/productpage/productpage-dev-values.yaml

# Setup details service
helm install bookinfo-details-dev helm-chart/details --namespace bookinfo-dev -f helm-chart/details/details-dev-values.yaml

# Setup ratings service
helm install bookinfo-ratings-dev helm-chart/ratings --namespace bookinfo-dev -f helm-chart/ratings/ratings-dev-values.yaml

# Setup reviews service
helm install bookinfo-reviews-dev helm-chart/reviews --namespace bookinfo-dev -f helm-chart/reviews/reviews-dev-values.yaml
```