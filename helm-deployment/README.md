# Helm Deployment

This directory contains a Helm chart to deploy the microservices project.

## Components
The Helm chart provisions:
- PostgreSQL database (with initialization ConfigMap and PVC)
- Catalog Service
- Orders Service
- UI Service

## Prerequisites
1. A running Kubernetes cluster.
2. Helm installed on your machine.
3. The Docker images must be built and available in your cluster.

## Deployment
From the directory containing this chart, you can deploy using Helm:
```bash
helm install my-release .
```

To customize values, you can edit `values.yaml` or provide overriding values:
```bash
helm install my-release . --set ui.nodePort=30090
```

## Uninstallation
```bash
helm uninstall my-release
```
