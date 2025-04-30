# Deploying a Flask App with PostgreSQL on Kubernetes

This guide outlines the process of deploying a Flask application connected to a PostgreSQL database in a Kubernetes cluster. The setup includes a namespace, ConfigMap, Secret, Services, and Ingress for external access, following real-world Kubernetes deployment practices.

## Step 1: Create a Namespace
**Command**: `kubectl create namespace flask-postgres-app`

**What Happens**:
- The user submits the command via `kubectl`, sending the request to the Kubernetes APIServer.
- The APIServer validates and stores the new namespace (`flask-postgres-app`) in etcd.
- The namespace isolates resources for this application within the cluster.

## Step 2: Deploy a ConfigMap for Flask App Configuration
**Command**: `kubectl apply -f configmap.yaml -n flask-postgres-app`

**ConfigMap Content**: Defines environment variables for the Flask app (e.g., database connection details).

**What Happens**:
- The user submits the ConfigMap YAML to the APIServer.
- The APIServer stores the ConfigMap (`flask-config`) in etcd.
- The ConfigMap is available in the `flask-postgres-app` namespace for use by Flask app Pods.

## Step 3: Deploy a Secret for PostgreSQL Credentials
**Command**: `kubectl apply -f secret.yaml -n flask-postgres-app`

**Secret Content**: Stores PostgreSQL credentials (e.g., username, password) in encrypted form.

**What Happens**:
- The user submits the Secret YAML to the APIServer.
- The APIServer encrypts and stores the Secret (`postgres-secret`) in etcd.
- The Secret is available in the namespace for secure use by PostgreSQL.

## Step 4: Deploy PostgreSQL
**Command**: `kubectl apply -f postgres-deployment.yaml -n flask-postgres-app`

**Deployment Content**: Defines a PostgreSQL Deployment with 1 replica, a PersistentVolumeClaim for storage, and environment variables from the Secret.

**What Happens**:
- The user submits the Deployment YAML to the APIServer.
- The APIServer stores the Deployment in etcd.
- The ControllerManager creates a ReplicaSet for the Deployment (`postgres-deployment`) to ensure 1 Pod runs.
- The Scheduler assigns the Pod to a Node in a NodePool based on resource availability.
- The Kubelet on the assigned Node uses the ContainerRuntime to pull the PostgreSQL image (e.g., `postgres:15`) and start the Pod.
- The Pod requests storage via a PersistentVolumeClaim (`postgres-pvc`), binding to a PersistentVolume provisioned by a StorageClass (e.g., `standard`).
- The Pod mounts the PersistentVolume for data storage (e.g., `/var/lib/postgresql/data`) and uses credentials from the Secret (`postgres-secret`) to initialize the database.

## Step 5: Deploy the Flask App
**Command**: `kubectl apply -f flask-deployment.yaml -n flask-postgres-app`

**Deployment Content**: Defines a Flask app Deployment with 3 replicas, using the ConfigMap for configuration and connecting to PostgreSQL.

**What Happens**:
- The user submits the Deployment YAML to the APIServer.
- The APIServer stores the Deployment in etcd.
- The ControllerManager creates a ReplicaSet for the Deployment (`flask-deployment`) to ensure 3 Pods run.
- The Scheduler assigns Pods to Nodes in a NodePool.
- The Kubelet on each Node uses the ContainerRuntime to pull the Flask app image (e.g., `flask-app:1.0`) and start the Pods.
- The Pods load configuration (e.g., database host) from the ConfigMap (`flask-config`) and connect to PostgreSQL via the Service.

## Step 6: Create a Service for PostgreSQL
**Command**: `kubectl apply -f postgres-service.yaml -n flask-postgres-app`

**Service Content**: Exposes PostgreSQL on a ClusterIP (e.g., `postgres-service`) for internal communication.

**What Happens**:
- The user submits the Service YAML to the APIServer.
- The APIServer stores the Service in etcd.
- The Service (`postgres-service`) is assigned a ClusterIP, and KubeProxy configures networking rules to route traffic to the PostgreSQL Pod.
- CoreDNS registers the Service name (`postgres-service.flask-postgres-app.svc.cluster.local`), enabling Flask Pods to connect to PostgreSQL.

## Step 7: Create a Service for Flask App
**Command**: `kubectl apply -f flask-service.yaml -n flask-postgres-app`

**Service Content**: Exposes the Flask app on a ClusterIP (e.g., `flask-service`) for load balancing across Pods.

**What Happens**:
- The user submits the Service YAML to the APIServer.
- The APIServer stores the Service in etcd.
- The Service (`flask-service`) gets a ClusterIP, and KubeProxy configures load balancing across the 3 Flask Pods.
- CoreDNS registers the Service name (`flask-service.flask-postgres-app.svc.cluster.local`).

## Step 8: Create an Ingress for External Access
**Command**: `kubectl apply -f ingress.yaml -n flask-postgres-app`

**Ingress Content**: Routes external traffic (e.g., `app.example.com`) to the Flask Service.

**What Happens**:
- The user submits the Ingress YAML to the APIServer.
- The APIServer stores the Ingress in etcd.
- The IngressController (e.g., NGINX) processes the Ingress rules, setting up an external load balancer or proxy to route traffic from `app.example.com` to the Service (`flask-service`), which load-balances to the Flask Pods.

## Step 9: Scaling and Monitoring
**What Happens**:
- The MetricsServer collects CPU/memory usage from Flask and PostgreSQL Pods.
- If traffic spikes, the ClusterAutoscaler may add Nodes to the NodePool, and the Scheduler assigns new Pods if the Deployment scales (e.g., from 3 to 5 replicas).
- If a Flask Pod fails, the ReplicaSet creates a replacement, and the Scheduler reassigns it to a healthy Node.

## Step 10: End-to-End Functionality
**What Happens**:
- External users access the Flask app via `app.example.com`, routed by the IngressController to the Service (`flask-service`), which load-balances to the Flask Pods.
- The Flask app connects to PostgreSQL using the Service (`postgres-service`), resolved by CoreDNS, and performs database operations with data stored on the PersistentVolume.
