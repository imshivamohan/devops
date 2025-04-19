# Simplified Helm Cheat Sheet with Nginx Examples

This Markdown file provides a simplified Helm cheat sheet for students, using a basic Nginx web server (`nginx:latest`) instead of a Flask-PostgreSQL app. It covers 18 Helm concepts, with clear examples, test commands, and screenshot placeholders, tailored for a MicroK8s environment in the `webapp` namespace. Use this as a teaching resource alongside the Kubernetes and Helm slide deck (April 18, 2025) for hands-on learning.

---

## 1. Installation
**Description**: Installs the Helm CLI to manage charts in Kubernetes.
**Example**:
```bash
sudo apt-get install helm
helm version
```
**Test Command**: `helm list -A`
**Screenshot Placeholder**:
- Capture: `helm list -A`
- Description: Show empty release list to confirm Helm is installed.
**Notes**: Run on Ubuntu in MicroK8s. Verifies Helm is ready for Nginx deployments.

---

## 2. Chart Structure
**Description**: Defines the directory layout of a Helm chart, bundling Kubernetes manifests.
**Example**:
```
nginx-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
└── charts/
```
**Test Command**: `helm create nginx-chart && tree nginx-chart`
**Screenshot Placeholder**:
- Capture: `tree nginx-chart`
- Description: Show chart directory structure.
**Notes**: Creates a chart for deploying Nginx. `Chart.yaml` defines metadata; `templates/` holds YAMLs.

---

## 3. Installing and Upgrading
**Description**: Installs a chart as a release or upgrades an existing release.
**Example**:
```bash
helm install nginx-release ./nginx-chart -n webapp
helm upgrade nginx-release ./nginx-chart -n webapp
```
**Test Command**: `helm list -n webapp`
**Screenshot Placeholder**:
- Capture: `helm list -n webapp`
- Description: Show `nginx-release` in the output.
**Notes**: Installs Nginx in `webapp`. Upgrade applies chart changes (e.g., updated values).

---

## 4. Values Files
**Description**: Customizes chart deployments via a `values.yaml` file.
**Example**:
```yaml
nginx:
  replicas: 2
  image: nginx:latest
  port: 80
```
**Test Command**: `helm install nginx-release ./nginx-chart -f values.yaml -n webapp`
**Screenshot Placeholder**:
- Capture: `helm get values nginx-release -n webapp`
- Description: Show applied values (e.g., `replicas: 2`).
**Notes**: Configures Nginx replicas and image. Students can edit `values.yaml` for customization.

---

## 5. Repositories
**Description**: Stores and shares Helm charts, like an app store.
**Example**:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install nginx-bitnami bitnami/nginx -n webapp
```
**Test Command**: `helm search repo bitnami/nginx`
**Screenshot Placeholder**:
- Capture: `helm repo list`
- Description: Show Bitnami repo in the output.
**Notes**: Installs Nginx from Bitnami repo. Simplifies accessing pre-built charts.

---

## 6. Templates
**Description**: Uses Go templating to generate dynamic Kubernetes manifests.
**Example** (in `templates/deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
  namespace: {{ .Release.Namespace }}
spec:
  replicas: {{ .Values.nginx.replicas }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: {{ .Values.nginx.image }}
        ports:
        - containerPort: {{ .Values.nginx.port }}
```
**Test Command**: `helm get manifest nginx-release -n webapp`
**Screenshot Placeholder**:
- Capture: `helm get manifest nginx-release -n webapp | grep nginx`
- Description: Show rendered Nginx Deployment.
**Notes**: Dynamically sets replicas, image, and port based on `values.yaml`.

---

## 7. Chart Dependencies
**Description**: Includes other charts as dependencies for modular apps.
**Example** (in `Chart.yaml`):
```yaml
dependencies:
- name: nginx
  version: 15.x.x
  repository: https://charts.bitnami.com/bitnami
```
**Test Command**: `helm dependency update ./nginx-chart`
**Screenshot Placeholder**:
- Capture: `helm dependency list ./nginx-chart`
- Description: Show Nginx dependency in the output.
**Notes**: Adds Bitnami’s Nginx chart as a dependency. Simplifies bundling related components.

---

## 8. Rollbacks
**Description**: Reverts a release to a previous version if an upgrade fails.
**Example**:
```bash
helm rollback nginx-release 1 -n webapp
```
**Test Command**: `helm history nginx-release -n webapp`
**Screenshot Placeholder**:
- Capture: `helm history nginx-release -n webapp`
- Description: Show release history with rollback.
**Notes**: Restores Nginx to a stable state. Useful for fixing bad deployments.

---

## 9. Hooks
**Description**: Executes tasks during a release’s lifecycle (e.g., pre-install).
**Example** (in `templates/pre-install-job.yaml`):
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-pre-install
  namespace: {{ .Release.Namespace }}
  annotations:
    "helm.sh/hook": pre-install
spec:
  template:
    spec:
      containers:
      - name: setup
        image: busybox
        command: ["echo", "Setting up Nginx"]
      restartPolicy: Never
```
**Test Command**: `kubectl get jobs -n webapp`
**Screenshot Placeholder**:
- Capture: `kubectl get jobs -n webapp`
- Description: Show `nginx-release-pre-install` Job.
**Notes**: Runs a simple echo command before Nginx install. Demonstrates lifecycle automation.

---

## 10. Custom Resource Definitions (CRDs)
**Description**: Manages custom Kubernetes resources in charts.
**Example** (in `templates/crd-example.yaml`):
```yaml
apiVersion: example.com/v1
kind: SimpleWeb
metadata:
  name: {{ .Release.Name }}-web
  namespace: {{ .Release.Namespace }}
spec:
  image: {{ .Values.nginx.image }}
  replicas: {{ .Values.nginx.replicas }}
```
**Test Command**: `kubectl get simplewebs -n webapp`
**Screenshot Placeholder**:
- Capture: `kubectl get simplewebs -n webapp`
- Description: Show `nginx-release-web` CRD (if CRD is applied).
**Notes**: Hypothetical CRD for Nginx. Shows how Helm handles custom resources.

---

## 11. Plugins
**Description**: Extends Helm with additional functionality.
**Example**:
```bash
helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade nginx-release ./nginx-chart -n webapp
```
**Test Command**: `helm diff upgrade nginx-release ./nginx-chart -n webapp`
**Screenshot Placeholder**:
- Capture: `helm diff upgrade nginx-release ./nginx-chart -n webapp`
- Description: Show diff output for Nginx chart changes.
**Notes**: `helm-diff` previews upgrades. Simplifies debugging chart changes.

---

## 12. Secrets Management
**Description**: Secures sensitive data in charts using Kubernetes Secrets.
**Example** (in `templates/secret.yaml`):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ .Release.Name }}-nginx-secret
  namespace: {{ .Release.Namespace }}
type: Opaque
stringData:
  nginx-config: {{ .Values.nginx.config | quote }}
```
**Test Command**: `kubectl get secrets -n webapp`
**Screenshot Placeholder**:
- Capture: `kubectl get secrets -n webapp`
- Description: Show `nginx-release-nginx-secret`.
**Notes**: Stores Nginx config (e.g., `nginx.conf`). Demonstrates secure data handling.

---

## 13. Subcharts
**Description**: Organizes complex apps into modular subcharts.
**Example**:
```
nginx-chart/
├── charts/
│   ├── nginx-subchart/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── templates/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
├── Chart.yaml
├── values.yaml
```
**Test Command**: `helm install nginx-release ./nginx-chart -n webapp`
**Screenshot Placeholder**:
- Capture: `helm list -n webapp`
- Description: Show `nginx-release` with subchart.
**Notes**: Separates Nginx into a subchart. Simplifies managing multi-component apps.

---

## 14. Library Charts
**Description**: Provides reusable templates for multiple charts.
**Example** (in `charts/common/templates/_labels.tpl`):
```yaml
{{- define "common.labels" -}}
app: {{ .Release.Name }}
chart: {{ .Chart.Name }}
{{- end -}}
```
**Test Command**: `kubectl get deployments -n webapp -o yaml`
**Screenshot Placeholder**:
- Capture: `kubectl get deployments -n webapp -o yaml | grep labels`
- Description: Show Nginx Deployment with common labels.
**Notes**: Applies standard labels to Nginx. Reduces code duplication.

---

## 15. Post-Renderers
**Description**: Modifies rendered manifests before application.
**Example** (in `post-renderer.sh`):
```bash
#!/bin/bash
cat - | sed 's/podAnnotations: {}/podAnnotations: { custom: "nginx" }/'
```
**Test Command**: `helm install nginx-release ./nginx-chart --post-renderer ./post-renderer.sh -n webapp`
**Screenshot Placeholder**:
- Capture: `kubectl get pods -n webapp -o yaml | grep custom`
- Description: Show `custom: nginx` annotation on Nginx Pods.
**Notes**: Adds a custom annotation to Nginx Pods. Shows advanced customization.

---

## 16. Provenance and Integrity
**Description**: Ensures chart authenticity via signing and verification.
**Example**:
```bash
helm package ./nginx-chart --sign --key "Your Name"
helm verify nginx-chart-0.1.0.tgz
```
**Test Command**: `helm verify nginx-chart-0.1.0.tgz`
**Screenshot Placeholder**:
- Capture: `helm verify nginx-chart-0.1.0.tgz`
- Description: Show verification output.
**Notes**: Secures Nginx chart distribution. Introduces GPG signing.

---

## 17. Debugging
**Description**: Troubleshoots chart issues with dry-run and linting.
**Example**:
```bash
helm lint ./nginx-chart
helm install nginx-release ./nginx-chart --dry-run -n webapp
```
**Test Command**: `helm install nginx-release ./nginx-chart --dry-run -n webapp`
**Screenshot Placeholder**:
- Capture: `helm install nginx-release ./nginx-chart --dry-run -n webapp | head -n 20`
- Description: Show dry-run output for Nginx chart.
**Notes**: Validates Nginx chart before deployment. Helps catch errors early.

---

## 18. Best Practices
**Description**: Guidelines for effective Helm usage.
**Example**:
- Version charts in `Chart.yaml` (e.g., `version: 0.1.0`).
- Use `values.yaml` for all configurable options.
- Test charts with `helm lint` and `helm install --dry-run`.
- Organize complex apps with subcharts.
- Secure sensitive data with Secrets.
**Test Command**: `helm lint ./nginx-chart`
**Screenshot Placeholder**:
- Capture: `helm lint ./nginx-chart`
- Description: Show linting output with no errors.
**Notes**: Ensures robust Nginx chart development. Encourages clean, reusable code.

---
