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

## Setup worload identity for jenkins worker
### Update cluster
```
gcloud container node-pools update [POOL_NAME] \
    --cluster=[CLUSTER_NAME] \
    --zone=[ZONE] \
    --workload-metadata=GKE_METADATA
```

### Setup workload identity
```
# 1. Create the GSA
gcloud iam service-accounts create jenkins-gke-deployer

# 2. Grant it permission to manage GKE
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:jenkins-gke-deployer@[PROJECT_ID].iam.gserviceaccount.com" \
  --role="roles/container.developer"

# 3. Allow KSA to impersonate GSA (The Workload Identity Link)
gcloud iam service-accounts add-iam-policy-binding \
  jenkins-gke-deployer@[PROJECT_ID].iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:[PROJECT_ID].svc.id.goog[devops-tools/jenkins-deployer]"

# 4. Annotate the KSA
kubectl annotate serviceaccount jenkins-deployer \
  --namespace devops-tools \
  iam.gke.io/gcp-service-account=jenkins-gke-deployer@[PROJECT_ID].iam.gserviceaccount.com
```

### Apply rbac for namespaces
```
kubectl apply -f devops-tools/jenkins-rbac.yaml -n bookinfo-dev
```

### Checking authorization
```
kubectl auth can-i create deployments \
  --namespace prod \
  --as system:serviceaccount:devops-tools:jenkins-deployer
```