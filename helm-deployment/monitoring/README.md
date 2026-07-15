# Monitoring Setup (Prometheus, Grafana, Loki)

This directory contains the necessary instructions and configuration to deploy a complete observability stack into your Kubernetes cluster in the simplest way possible.

We use the official, highly-optimized community Helm charts:
- `kube-prometheus-stack`: Provides Prometheus, Grafana, and pre-configured dashboards for Kubernetes cluster metrics.
- `loki-stack`: Provides Loki (log storage) and Promtail (log collection from all pods).

---

## 🛠️ Installation Steps

Run the following commands from this directory (`helm-deployment/monitoring/`).

### 1. Add the required Helm Repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### 2. Create a Dedicated Namespace

It's best practice to keep monitoring tools in their own namespace to keep things clean.

```bash
kubectl create namespace monitoring
```

### 3. Install Prometheus & Grafana

Install the `kube-prometheus-stack`. We pass the `grafana-values.yaml` file to ensure Grafana automatically connects to Loki out-of-the-box.

```bash
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f grafana-values.yaml
```

*Note: This might take a minute or two to pull the images and start all the pods.*

### 4. Install Loki & Promtail

Install the `loki-stack`. Promtail will automatically start scraping logs from all your microservices and sending them to Loki.

```bash
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  --set grafana.enabled=false,loki.isDefault=false
```
*(We set `grafana.enabled=false` because we are already using the Grafana instance from the Prometheus stack!)*

---

## 🚀 Accessing the Dashboards

Once all pods in the `monitoring` namespace are running (`kubectl get pods -n monitoring`), you can access the Grafana UI!

1. **Port-forward Grafana to your local machine:**
   ```bash
   kubectl port-forward service/prometheus-grafana 8080:80 -n monitoring
   ```

2. **Open your browser:**
   Go to: http://localhost:8080

3. **Login:**
   - **Username:** `admin`
   - **Password:** `prom-operator`

### What to check in Grafana:
- **Metrics (Prometheus):** Go to `Dashboards` -> `General` and look for the pre-installed Kubernetes dashboards (e.g., "Kubernetes / Compute Resources / Namespace (Pods)").
- **Logs (Loki):** Go to `Explore` (the compass icon on the left menu). In the top-left dropdown, select `Loki`. You can now query logs! 
   * Try entering `{app="my-release-catalog-service"}` or `{namespace="default"}` to see live logs from your microservices!
