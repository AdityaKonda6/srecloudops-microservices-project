# Kubernetes Deployment

This directory contains Kubernetes manifest files to deploy the microservices project.

## Components
- **postgres**: A stateful service running PostgreSQL with persistent storage and a ConfigMap for initialization.
- **catalog-service**: A stateless microservice.
- **orders-service**: A stateless microservice.
- **ui**: A stateless frontend microservice exposed via a NodePort service.

## Prerequisites
1. A running Kubernetes cluster (e.g., Minikube, kind, or cloud provider).
2. The Docker images must be built and available in the cluster. If you're using minikube, you can build them directly in minikube's Docker daemon:
   ```bash
   eval $(minikube docker-env)
   docker build -t catalog-service:latest -f ../catalog_service/Dockerfile ../
   docker build -t orders-service:latest -f ../orders_service/Dockerfile ../
   docker build -t ui:latest -f ../ui/Dockerfile ../
   ```

## Deployment
To deploy all services, run:
```bash
kubectl apply -f .
```

To view the UI, get the Node IP and access port 30080.
If using minikube, you can just run:
```bash
minikube service ui --url
```
