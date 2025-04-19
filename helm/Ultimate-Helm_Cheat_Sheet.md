# Ultimate-Helm_Cheat_Sheet for Students 🚀

This cheat sheet is designed for students learning Helm, the Kubernetes package manager, using a Flask application (`siva9989/employee-app`) connected to a PostgreSQL database (`postgres:14`) as a practical example. It covers **all major Helm concepts** from beginner to advanced: Installation, Chart Structure, Installing/Upgrading/Releasing, Values Files, Repositories, Templates, Built-in Objects, Chart Dependencies, Rollbacks, Chart Testing, Hooks, Custom Resource Definitions (CRDs), Plugins, Secrets Management, Subcharts, Library Charts, Post-Renderers, and Provenance and Integrity. Each concept includes:

- **Explanation**: Purpose and use case, tied to the Flask-PostgreSQL app.
- **Example**: Commands, YAML configurations, or directory structures with inline comments.
- **Usage**: How the concept is applied in the app.
- **Testing**: Step-by-step commands to verify functionality.
- **Dependencies**: Required tools or resources.

The **End-to-End Flow** provides a logical sequence for applying these concepts. All resources are scoped to the `webapp` namespace, and configurations are compatible with MicroK8s, using `microk8s-hostpath` for storage. The example deploys the Flask-PostgreSQL app, with a PostgreSQL table (`employees`) for employee management.

---

## **Prerequisites**

- **MicroK8s**: Installed and running (e.g., on Ubuntu, per April 9, 2025).
- **kubectl**: Configured to interact with MicroK8s (`microk8s kubectl`).
- **MicroK8s Add-ons**:
  - Enable Ingress: `microk8s enable ingress` for Ingress testing.
  - Enable MetalLB: `microk8s enable metallb:192.168.1.100-192.168.1.200` for LoadBalancer testing.
  - Enable Metrics Server: `microk8s enable metrics-server` for scaling tests.
- **Docker Hub Access**: Ensure `siva9989/employee-app:latest` and `postgres:14` images are accessible.
- **Tools**: `helm` (to be installed), `curl`, `psql`, and a text editor.
- **Basic Kubernetes Knowledge**: Familiarity with Pods, Deployments, Services, etc. (per Kubernetes cheat sheet, April 18, 2025).
- **Namespace**: `webapp` (created via `kubectl create namespace webapp`).

---

## **1️⃣ Helm Installation**

### **Explanation**
- **Purpose**: Installs Helm CLI to manage Kubernetes packages (charts).
- **Use Case**: Setting up Helm to deploy the Flask-PostgreSQL app.

### **Example**
```bash
# Install Helm on Ubuntu
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### **Usage**
- Enables Helm commands to create, install, and manage charts.
- Required for all Helm operations.

### **Testing**
1. Install Helm:
   ```bash
   helm version  # Should show v3.x.x
   ```
2. Verify:
   ```bash
   helm list -A  # Lists releases (empty initially)
   ```

### **Dependencies**
- None.

---

## **2️⃣ Chart Structure**

### **Explanation**
- **Purpose**: Defines the directory structure and files for a Helm chart.
- **Use Case**: Creating a chart for the Flask-PostgreSQL app.

### **Example**
```bash
helm create employee-app
```
Resulting structure:
```
employee-app/
├── Chart.yaml          # Chart metadata (name, version, etc.)
├── values.yaml         # Default configuration values
├── charts/             # Dependency charts
├── templates/          # Kubernetes manifests with templating
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── _helpers.tpl    # Template helpers
│   └── NOTES.txt       # Post-installation notes
└── .helmignore         # Files to ignore during packaging
```

### **Usage**
- Organizes Kubernetes manifests and configurations for the Flask app.
- Allows customization via `values.yaml`.

### **Testing**
1. Create a chart:
   ```bash
   mkdir helm-charts && cd helm-charts
   helm create employee-app
   ```
2. Verify:
   ```bash
   tree employee-app
   cat employee-app/Chart.yaml  # Shows metadata
   ```

### **Dependencies**
- Helm installed.

---

## **3️⃣ Installing/Upgrading/Releasing**

### **Explanation**
- **Purpose**: Manages Helm releases (instances of installed charts).
- **Use Case**: Deploying and updating the Flask-PostgreSQL app.

### **Example**
Create a custom chart for Flask:
```
employee-app/
├── Chart.yaml
│   # name: employee-app
│   # version: 0.1.0
├── values.yaml
│   # flask:
│   #   replicas: 2
│   #   image: siva9989/employee-app:latest
│   #   port: 5000
│   # postgres:
│   #   image: postgres:14
│   #   storage: 1Gi
└── templates/
    ├── flask-deployment.yaml
    │   # Standard Deployment with {{ .Values.flask }} templating
    ├── flask-service.yaml
    │   # NodePort Service
    ├── postgres-statefulset.yaml
    │   # StatefulSet with volumeClaimTemplates
    └── postgres-service.yaml
    │   # ClusterIP Service
```

Commands:
```bash
# Install
helm install employee-release ./employee-app -n webapp
# Upgrade
helm upgrade employee-release ./employee-app -n webapp
# Uninstall
helm uninstall employee-release -n webapp
```

### **Usage**
- Installs the Flask app and PostgreSQL as a release (`employee-release`).
- Upgrades apply changes without downtime.
- Uninstall removes the release.

### **Testing**
1. Create and install:
   ```bash
   helm create employee-app
   # Edit Chart.yaml, values.yaml, and templates/ as above
   kubectl create namespace webapp
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   helm list -n webapp  # Shows employee-release
   kubectl get pods -n webapp
   ```
3. Test:
   ```bash
   kubectl port-forward svc/flask-service 8080:80 -n webapp
   curl http://localhost:8080
   ```
4. Upgrade:
   ```bash
   # Edit values.yaml (e.g., replicas: 3)
   helm upgrade employee-release ./employee-app -n webapp
   kubectl get pods -n webapp  # Shows 3 replicas
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **4️⃣ Values Files**

### **Explanation**
- **Purpose**: Customizes chart deployments via configuration values.
- **Use Case**: Configuring Flask replicas and PostgreSQL credentials.

### **Example**
`employee-app/values.yaml`:
```yaml
flask:
  replicas: 2
  image: siva9989/employee-app:latest
  port: 5000
  env:
    DB_HOST: postgres-service
postgres:
  image: postgres:14
  storage: 1Gi
  secret:
    POSTGRES_DB: employee_db
    POSTGRES_USER: employee_user
    POSTGRES_PASSWORD: secret123
```

Override at install:
```bash
helm install employee-release ./employee-app -n webapp \
  --set flask.replicas=3 \
  -f custom-values.yaml
```

`custom-values.yaml`:
```yaml
flask:
  replicas: 3
  env:
    LOG_LEVEL: debug
```

### **Usage**
- Defines default settings in `values.yaml`.
- Overrides via `--set` or external YAML for flexibility.

### **Testing**
1. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp -f custom-values.yaml
   ```
2. Verify:
   ```bash
   helm get values employee-release -n webapp  # Shows applied values
   kubectl get deployments -n webapp  # Shows 3 replicas
   ```
3. Test:
   ```bash
   kubectl exec <flask-pod-name> -n webapp -- env  # Shows LOG_LEVEL=debug
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **5️⃣ Repositories**

### **Explanation**
- **Purpose**: Stores and shares Helm charts.
- **Use Case**: Adding a public repository to install PostgreSQL.

### **Example**
```bash
# Add Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
# Search for PostgreSQL
helm search repo bitnami/postgresql
# Install
helm install postgres-release bitnami/postgresql -n webapp
```

### **Usage**
- Accesses pre-built charts for PostgreSQL, reducing custom chart creation.
- Simplifies dependency management.

### **Testing**
1. Add and install:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   helm install postgres-release bitnami/postgresql -n webapp
   ```
2. Verify:
   ```bash
   helm list -n webapp
   kubectl get pods -n webapp
   ```
3. Test:
   ```bash
   kubectl exec -it <postgres-pod-name> -n webapp -- psql -U postgres
   ```

### **Dependencies**
- Namespace (`webapp`).

---

## **6️⃣ Templates**

### **Explanation**
- **Purpose**: Uses Go templating to generate Kubernetes manifests dynamically.
- **Use Case**: Creating a dynamic Flask Deployment.

### **Example**
`employee-app/templates/flask-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-flask
  namespace: {{ .Release.Namespace }}
spec:
  replicas: {{ .Values.flask.replicas }}
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: {{ .Values.flask.image }}
        ports:
        - containerPort: {{ .Values.flask.port }}
        env:
        {{- range $key, $value := .Values.flask.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
```

### **Usage**
- Dynamically generates manifests based on `values.yaml`.
- Reduces hardcoding and enhances reusability.

### **Testing**
1. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   helm get manifest employee-release -n webapp | grep flask-deployment
   kubectl describe deployment employee-release-flask -n webapp
   ```
3. Test:
   ```bash
   # Edit values.yaml (e.g., flask.env.LOG_LEVEL=info)
   helm upgrade employee-release ./employee-app -n webapp
   kubectl exec <flask-pod-name> -n webapp -- env
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **7️⃣ Built-in Objects**

### **Explanation**
- **Purpose**: Provides access to Helm context (e.g., release, chart, values).
- **Use Case**: Using `.Release.Name` and `.Values` in templates.

### **Example**
`employee-app/templates/_helpers.tpl`:
```yaml
{{- define "employee-app.labels" -}}
app: {{ .Release.Name }}-flask
chart: {{ .Chart.Name }}-{{ .Chart.Version }}
release: {{ .Release.Name }}
{{- end -}}
```

`employee-app/templates/flask-deployment.yaml`:
```yaml
metadata:
  labels:
    {{- include "employee-app.labels" . | nindent 4 }}
spec:
  template:
    metadata:
      labels:
        {{- include "employee-app.labels" . | nindent 8 }}
```

### **Usage**
- Standardizes labels across resources.
- Accesses `.Release`, `.Chart`, and `.Values` for dynamic configuration.

### **Testing**
1. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   kubectl get deployments -n webapp -o yaml | grep labels
   ```
3. Test:
   ```bash
   helm upgrade employee-release ./employee-app -n webapp --set flask.replicas=4
   kubectl describe deployment employee-release-flask -n webapp
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **8️⃣ Chart Dependencies**

### **Explanation**
- **Purpose**: Includes other charts as dependencies.
- **Use Case**: Using Bitnami’s PostgreSQL chart in the Flask app.

### **Example**
`employee-app/Chart.yaml`:
```yaml
dependencies:
- name: postgresql
  version: 12.x.x
  repository: https://charts.bitnami.com/bitnami
```

`employee-app/values.yaml`:
```yaml
postgresql:
  auth:
    database: employee_db
    username: employee_user
    password: secret123
```

Update dependencies:
```bash
helm dependency update ./employee-app
```

### **Usage**
- Bundles PostgreSQL as a dependency, simplifying database setup.
- Configures via `values.yaml`.

### **Testing**
1. Update and install:
   ```bash
   helm dependency update ./employee-app
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   helm list -n webapp
   kubectl get pods -n webapp  # Shows Flask and PostgreSQL
   ```
3. Test:
   ```bash
   kubectl exec -it <postgres-pod-name> -n webapp -- psql -U employee_user -d employee_db
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).
- Bitnami repository.

---

## **9️⃣ Rollbacks**

### **Explanation**
- **Purpose**: Reverts a release to a previous version.
- **Use Case**: Reverting a faulty Flask app upgrade.

### **Example**
```bash
# Install
helm install employee-release ./employee-app -n webapp
# Upgrade (introduces error, e.g., wrong image)
helm upgrade employee-release ./employee-app -n webapp --set flask.image=wrong-image
# Rollback
helm rollback employee-release 1 -n webapp
```

### **Usage**
- Restores a stable release state.
- Maintains deployment reliability.

### **Testing**
1. Apply and break:
   ```bash
   helm install employee-release ./employee-app -n webapp
   helm upgrade employee-release ./employee-app -n webapp --set flask.image=nonexistent:latest
   kubectl get pods -n webapp  # Shows crash
   ```
2. Rollback:
   ```bash
   helm rollback employee-release 1 -n webapp
   ```
3. Verify:
   ```bash
   helm history employee-release -n webapp
   kubectl get pods -n webapp  # Shows running pods
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **10️⃣ Chart Testing**

### **Explanation**
- **Purpose**: Validates chart integrity and deployment.
- **Use Case**: Ensuring the Flask chart is correctly formatted.

### **Example**
`employee-app/templates/tests/test-connection.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ .Release.Name }}-flask:80']
  restartPolicy: Never
```

### **Usage**
- Runs a test pod to verify Flask Service connectivity.
- Ensures chart functionality.

### **Testing**
1. Add test and install:
   ```bash
   # Add test-connection.yaml to templates/
   helm install employee-release ./employee-app -n webapp
   ```
2. Run test:
   ```bash
   helm test employee-release -n webapp
   ```
3. Verify:
   ```bash
   kubectl logs employee-release-test-connection -n webapp
   kubectl get pods -n webapp
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **11️⃣ Helm Hooks**

### **Explanation**
- **Purpose**: Executes tasks at specific release lifecycle stages (e.g., pre-install, post-upgrade).
- **Use Case**: Initializing the PostgreSQL `employees` table before Flask starts.

### **Example**
`employee-app/templates/db-init-job.yaml`:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-db-init
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: db-init
        image: postgres:14
        command: ["psql", "-h", "{{ .Release.Name }}-postgresql", "-U", "employee_user", "-d", "employee_db", "-c", "CREATE TABLE IF NOT EXISTS employees (id SERIAL PRIMARY KEY, name TEXT, email TEXT, role TEXT);"]
        env:
        - name: PGPASSWORD
          value: secret123
      restartPolicy: Never
```

### **Usage**
- Runs a Job to initialize the database before installation.
- Deletes the Job after success.

### **Testing**
1. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   kubectl get jobs -n webapp
   kubectl logs <job-pod-name> -n webapp
   ```
3. Test:
   ```bash
   kubectl exec -it <postgres-pod-name> -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).
- PostgreSQL dependency.

---

## **12️⃣ Custom Resource Definitions (CRDs)**

### **Explanation**
- **Purpose**: Manages CRDs as part of a chart (per your Kafka interest, March 30, 2025).
- **Use Case**: Including a Kafka CRD for event logging.

### **Example**
`employee-app/crds/kafka-crd.yaml`:
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: {{ .Release.Name }}-kafka
spec:
  kafka:
    replicas: 1
    listeners:
    - name: plain
      port: 9092
      type: internal
      tls: false
    storage:
      type: ephemeral
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
```

`employee-app/Chart.yaml`:
```yaml
annotations:
  helm.sh/keep-crds: "true"
```

### **Usage**
- Deploys Kafka alongside Flask for logging employee actions.
- Preserves CRDs on uninstall.

### **Testing**
1. Install Strimzi CRDs:
   ```bash
   kubectl apply -f https://strimzi.io/install/latest?namespace=webapp
   ```
2. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
3. Verify:
   ```bash
   kubectl get kafka -n webapp
   kubectl get pods -n webapp -l strimzi.io/cluster=employee-release-kafka
   ```
4. Test:
   ```bash
   kubectl run kafka-client --rm -it --image=strimzi/kafka:latest-kafka-3.4.0 --namespace=webapp -- bash
   kafka-topics.sh --bootstrap-server employee-release-kafka:9092 --create --topic employee-events
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).
- Strimzi CRDs.

---

## **13️⃣ Plugins**

### **Explanation**
- **Purpose**: Extends Helm with custom functionality.
- **Use Case**: Using `helm-diff` to preview chart changes.

### **Example**
```bash
# Install helm-diff plugin
helm plugin install https://github.com/databus23/helm-diff
# Preview changes
helm diff upgrade employee-release ./employee-app -n webapp
```

### **Usage**
- Shows differences before upgrading the Flask app.
- Improves deployment confidence.

### **Testing**
1. Install:
   ```bash
   helm plugin install https://github.com/databus23/helm-diff
   ```
2. Test:
   ```bash
   helm install employee-release ./employee-app -n webapp
   # Edit values.yaml (e.g., flask.replicas=4)
   helm diff upgrade employee-release ./employee-app -n webapp
   ```
3. Verify:
   ```bash
   helm upgrade employee-release ./employee-app -n webapp
   kubectl get deployments -n webapp
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **14️⃣ Secrets Management**

### **Explanation**
- **Purpose**: Securely manages sensitive data in charts.
- **Use Case**: Storing PostgreSQL credentials.

### **Example**
`employee-app/templates/secret.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ .Release.Name }}-postgres-secret
type: Opaque
stringData:
  POSTGRES_DB: {{ .Values.postgres.secret.POSTGRES_DB }}
  POSTGRES_USER: {{ .Values.postgres.secret.POSTGRES_USER }}
  POSTGRES_PASSWORD: {{ .Values.postgres.secret.POSTGRES_PASSWORD }}
```

Use in `postgres-statefulset.yaml`:
```yaml
env:
- name: POSTGRES_DB
  valueFrom:
    secretKeyRef:
      name: {{ .Release.Name }}-postgres-secret
      key: POSTGRES_DB
```

### **Usage**
- Secures database credentials.
- Integrates with Helm’s templating.

### **Testing**
1. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   kubectl get secrets -n webapp
   kubectl describe secret employee-release-postgres-secret -n webapp
   ```
3. Test:
   ```bash
   kubectl exec <postgres-pod-name> -n webapp -- env | grep POSTGRES
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **15️⃣ Subcharts**

### **Explanation**
- **Purpose**: Organizes complex apps into modular charts.
- **Use Case**: Separating Flask and PostgreSQL into subcharts.

### **Example**
```
employee-app/
├── Chart.yaml
├── values.yaml
├── charts/
│   ├── flask/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   └── postgresql/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── statefulset.yaml
│           └── service.yaml
```

`employee-app/Chart.yaml`:
```yaml
dependencies:
- name: flask
  version: 0.1.0
  condition: flask.enabled
- name: postgresql
  version: 0.1.0
  condition: postgresql.enabled
```

### **Usage**
- Modularizes Flask and PostgreSQL deployments.
- Enables independent configuration.

### **Testing**
1. Package subcharts:
   ```bash
   helm dependency build ./employee-app
   ```
2. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp
   ```
3. Verify:
   ```bash
   helm list -n webapp
   kubectl get all -n webapp
   ```
4. Test:
   ```bash
   kubectl port-forward svc/employee-release-flask 8080:80 -n webapp
   curl http://localhost:8080
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **16️⃣ Library Charts**

### **Explanation**
- **Purpose**: Provides reusable templates for multiple charts.
- **Use Case**: Defining common labels for Flask and PostgreSQL.

### **Example**
```
common/
├── Chart.yaml
│   # type: library
└── templates/
    └── _labels.tpl
        {{- define "common.labels" -}}
        app: {{ .Release.Name }}
        chart: {{ .Chart.Name }}
        {{- end -}}
```

`employee-app/Chart.yaml`:
```yaml
dependencies:
- name: common
  version: 0.1.0
  repository: file://../common
```

Use in `flask-deployment.yaml`:
```yaml
metadata:
  labels:
    {{- include "common.labels" . | nindent 4 }}
```

### **Usage**
- Standardizes labels across Flask and PostgreSQL.
- Reduces template duplication.

### **Testing**
1. Create and use:
   ```bash
   helm dependency build ./employee-app
   helm install employee-release ./employee-app -n webapp
   ```
2. Verify:
   ```bash
   kubectl get deployments -n webapp -o yaml | grep labels
   ```
3. Test:
   ```bash
   helm upgrade employee-release ./employee-app -n webapp
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`, `common`).

---

## **17️⃣ Post-Renderers**

### **Explanation**
- **Purpose**: Modifies manifests after rendering.
- **Use Case**: Adding annotations to Flask Pods.

### **Example**
`post-renderer.sh`:
```bash
#!/bin/bash
cat - | sed 's/podAnnotations: {}/podAnnotations: { custom: "true" }/' > /tmp/modified.yaml
cat /tmp/modified.yaml
```

Install with post-renderer:
```bash
helm install employee-release ./employee-app -n webapp --post-renderer ./post-renderer.sh
```

### **Usage**
- Injects custom annotations dynamically.
- Useful for monitoring or compliance.

### **Testing**
1. Create `post-renderer.sh` and make executable:
   ```bash
   chmod +x post-renderer.sh
   ```
2. Apply:
   ```bash
   helm install employee-release ./employee-app -n webapp --post-renderer ./post-renderer.sh
   ```
3. Verify:
   ```bash
   kubectl get pods -n webapp -o yaml | grep custom
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).

---

## **18️⃣ Provenance and Integrity**

### **Explanation**
- **Purpose**: Ensures chart authenticity and integrity via signing.
- **Use Case**: Signing the Flask chart for secure distribution.

### **Example**
```bash
# Generate GPG key (if needed)
gpg --generate-key
# Package and sign
helm package employee-app --sign --key "Your Name" --keyring ~/.gnupg/secring.gpg
# Verify
helm verify employee-app-0.1.0.tgz
```

### **Usage**
- Secures chart distribution.
- Verifies chart hasn’t been tampered with.

### **Testing**
1. Package and sign:
   ```bash
   helm package employee-app
   helm package employee-app --sign --key "Your Name" --keyring ~/.gnupg/secring.gpg
   ```
2. Verify:
   ```bash
   helm verify employee-app-0.1.0.tgz
   ```
3. Test:
   ```bash
   helm install employee-release employee-app-0.1.0.tgz -n webapp
   ```

### **Dependencies**
- Namespace (`webapp`).
- Helm chart (`employee-app`).
- GPG installed.

---

## **End-to-End Flow**

### **Setup**
1. Install Helm:
   ```bash
   sudo apt-get install helm
   ```
2. Create namespace:
   ```bash
   kubectl create namespace webapp
   ```

### **Chart Development and Deployment**
1. **Create Chart**:
   ```bash
   mkdir helm-charts && cd helm-charts
   helm create employee-app
   # Edit Chart.yaml, values.yaml, templates/ for Flask and PostgreSQL
   ```
2. **Add Dependencies**:
   ```bash
   helm dependency update ./employee-app
   ```
3. **Add Library Chart**:
   ```bash
   # Create common/ and update Chart.yaml
   helm dependency build ./employee-app
   ```
4. **Install Release**:
   ```bash
   helm install employee-release ./employee-app -n webapp -f custom-values.yaml
   ```
5. **Test Chart**:
   ```bash
   helm test employee-release -n webapp
   ```
6. **Upgrade with Post-Renderer**:
   ```bash
   # Create post-renderer.sh
   helm upgrade employee-release ./employee-app -n webapp --post-renderer ./post-renderer.sh
   ```
7. **Rollback (if needed)**:
   ```bash
   helm rollback employee-release 1 -n webapp
   ```
8. **Sign and Verify**:
   ```bash
   helm package employee-app --sign --key "Your Name" --keyring ~/.gnupg/secring.gpg
   helm verify employee-app-0.1.0.tgz
   ```

### **Validation**
```bash
kubectl port-forward svc/employee-release-flask 8080:80 -n webapp
curl http://localhost:8080
kubectl exec -it <postgres-pod-name> -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"
```

### **Cleanup**
```bash
helm uninstall employee-release -n webapp
kubectl delete namespace webapp
```

---

## **Summary**
This cheat sheet consolidates all Helm concepts using a Flask-PostgreSQL app, providing:
- **Comprehensive Coverage**: From installation to advanced features like provenance.
- **Student-Friendly**: Clear explanations, examples, and tests for hands-on learning.
- **MicroK8s Compatibility**: Uses `microk8s-hostpath` and add-ons.
- **Practical Integration**: Leverages your `siva9989/employee-app`, PostgreSQL setup (April 4, 2025), and Kafka interest (March 30, 2025) for CRDs.
- **End-to-End Flow**: Logical sequence for chart development and deployment.

Use this in your classes to teach Helm effectively, complementing your Kubernetes expertise! 🚀