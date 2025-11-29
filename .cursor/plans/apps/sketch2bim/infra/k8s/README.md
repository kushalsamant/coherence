# Kubernetes Deployment

Kubernetes deployment manifests and guides for Sketch-to-BIM.

## Overview

These Kubernetes manifests allow you to deploy Sketch-to-BIM on any Kubernetes cluster (GKE, EKS, DigitalOcean Kubernetes, self-hosted, etc.).

## Prerequisites

1. **Kubernetes Cluster** - Any k8s 1.20+ cluster
2. **kubectl** - Configured to access your cluster
3. **Docker Registry** - For container images (Docker Hub, GCR, ECR, etc.)

## Quick Start

### 1. Build and Push Docker Image

```bash
# Build image
cd backend
docker build -t your-registry/sketch2bim-backend:latest .

# Push to registry
docker push your-registry/sketch2bim-backend:latest
```

### 2. Create Secrets

```bash
# Create namespace
kubectl create namespace sketch2bim

# Create secrets
kubectl create secret generic sketch2bim-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=redis-url="redis://..." \
  --from-literal=secret-key="..." \
  --from-literal=razorpay-key-id="..." \
  --from-literal=razorpay-key-secret="..." \
  -n sketch2bim
```

### 3. Update Manifests

Edit `backend-deployment.yaml`:
- Update image name to your registry
- Adjust resource limits if needed
- Update environment variable references

### 4. Deploy

```bash
kubectl apply -f infra/k8s/
```

## Files

- **`backend-deployment.yaml`** - Backend API deployment
- **`backend-service.yaml`** - Backend service (LoadBalancer/NodePort)
- **`hpa.yaml`** - Horizontal Pod Autoscaler for auto-scaling

## Cluster Providers

### Google Cloud GKE

```bash
# Create cluster
gcloud container clusters create sketch2bim-cluster \
  --num-nodes=2 \
  --machine-type=e2-medium \
  --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials sketch2bim-cluster --zone=us-central1-a

# Deploy
kubectl apply -f infra/k8s/
```

### AWS EKS

```bash
# Create cluster (using eksctl)
eksctl create cluster \
  --name sketch2bim-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2

# Deploy
kubectl apply -f infra/k8s/
```

### DigitalOcean Kubernetes

```bash
# Create cluster via dashboard or doctl
doctl kubernetes cluster create sketch2bim-cluster \
  --region nyc1 \
  --size s-2vcpu-4gb \
  --count 2

# Get credentials
doctl kubernetes cluster kubeconfig save sketch2bim-cluster

# Deploy
kubectl apply -f infra/k8s/
```

### Self-Hosted (k3s/k8s)

```bash
# Install k3s (lightweight Kubernetes)
curl -sfL https://get.k3s.io | sh -

# Get kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml

# Deploy
kubectl apply -f infra/k8s/
```

## Configuration

### Resource Limits

Default resources in `backend-deployment.yaml`:
- **CPU**: 500m (0.5 cores) request, 2000m (2 cores) limit
- **Memory**: 1Gi request, 2Gi limit

Adjust based on your workload:
```yaml
resources:
  requests:
    cpu: "1000m"
    memory: "2Gi"
  limits:
    cpu: "4000m"
    memory: "4Gi"
```

### Scaling

#### Manual Scaling

```bash
kubectl scale deployment sketch2bim-backend --replicas=3 -n sketch2bim
```

#### Auto-Scaling (HPA)

The `hpa.yaml` file configures automatic scaling:
- Min replicas: 2
- Max replicas: 10
- CPU threshold: 70%

```bash
kubectl apply -f infra/k8s/hpa.yaml
```

### Environment Variables

Update environment variables in `backend-deployment.yaml`:

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: sketch2bim-secrets
        key: database-url
```

## Monitoring

### View Logs

```bash
# All pods
kubectl logs -f -l app=sketch2bim-backend -n sketch2bim

# Specific pod
kubectl logs -f <pod-name> -n sketch2bim
```

### View Metrics

```bash
# Pod status
kubectl get pods -n sketch2bim

# Resource usage
kubectl top pods -n sketch2bim
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n sketch2bim

# Check events
kubectl get events -n sketch2bim --sort-by='.lastTimestamp'
```

### Image Pull Errors

```bash
# Check if image exists
docker pull your-registry/sketch2bim-backend:latest

# Verify image pull secrets (if using private registry)
kubectl get secrets -n sketch2bim
```

### Database Connection Issues

```bash
# Test database connection from pod
kubectl exec -it <pod-name> -n sketch2bim -- python -c "from app.database import get_db; print('OK')"
```

## Cost Estimation

| Provider | Cluster Type | Cost/Month | Notes |
|----------|--------------|------------|-------|
| GKE | Standard | $70-150 | Managed, 2 nodes |
| EKS | Standard | $70-150 | Managed, 2 nodes |
| DigitalOcean | Managed | $24-48 | 2 nodes, simpler |
| k3s | Self-hosted | $10-20 | VPS cost only |

**Note**: Kubernetes is typically more expensive than single VPS but provides:
- High availability
- Auto-scaling
- Better resource utilization
- Production-grade reliability

## Next Steps

1. Set up ingress controller (nginx, traefik)
2. Configure SSL certificates (cert-manager)
3. Set up monitoring (Prometheus, Grafana)
4. Configure backups (Velero)
5. Set up CI/CD (ArgoCD, Flux)

## Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

