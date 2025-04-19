# Complete_Kubernetes_Cheat_Sheet_for_Flask-PostgreSQL_App 🚀

This cheat sheet is designed for students learning Kubernetes, using a Flask application (`siva9989/employee-app`) connected to a PostgreSQL database (`postgres:14`) as a practical example. It covers all major Kubernetes components: Namespace, Pod, Deployment, StatefulSet, Services (ClusterIP, Headless, LoadBalancer, NodePort), ConfigMap, Secret, Persistent Volume (PV), PersistentVolumeClaim (PVC), Job, CronJob, DaemonSet, Ingress, RBAC (Role and RoleBinding), and NetworkPolicy. Each component includes:

- **Explanation**: Purpose and use case, tied to the Flask-PostgreSQL app.
- **YAML Configuration**: Adapted from the provided example or created, with inline comments.
- **Usage**: How the component is used in the app (e.g., Secret in Flask and PostgreSQL).
- **Testing**: Step-by-step commands to verify functionality, using the Flask app and database.
- **Dependencies**: Required resources for the component or tests.

The **End-to-End Flow** provides a logical deployment and testing sequence, ensuring dependencies are met. All resources are scoped to the `webapp` namespace, and configurations are compatible with MicroK8s, using `microk8s-hostpath` or `hostPath` for storage. The example includes a PostgreSQL table (`employees`) to demonstrate database interaction.

---

## **Prerequisites**

- **MicroK8s**: Installed and running (e.g., on Ubuntu, per your context).
- **kubectl**: Installed and configured to interact with MicroK8s (`microk8s kubectl`).
- **MicroK8s Add-ons**:
  - Enable Ingress: `microk8s enable ingress` for Ingress testing.
  - Enable MetalLB: `microk8s enable metallb:192.168.1.100-192.168.1.200` for LoadBalancer testing.
  - Enable Calico (optional): For NetworkPolicy support, if not already enabled.
- **Docker Hub Access**: Ensure `siva9989/employee-app:latest` and `postgres:14` images are accessible.
- **Basic Tools**: `curl`, a browser, or a PostgreSQL client (e.g., `psql`) for testing.
- **User Setup**: A user (`student`) or service account for RBAC testing, with authentication configured.

---

## **1️⃣ Namespace**

### **Explanation**
- **Purpose**: Isolates resources within a cluster, preventing naming conflicts and enabling organization.
- **Use Case**: Grouping the Flask app and PostgreSQL resources in the `webapp` namespace for a clean environment.

### **YAML (`namespace.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Namespaces
kind: Namespace             # Defines the resource type as a Namespace
metadata:                   # Metadata section for the resource
  name: webapp              # Name of the namespace for the Flask-PostgreSQL app
```

### **Usage**
- Creates the `webapp` namespace to scope all application resources.
- Ensures isolation from other projects or namespaces.

### **Testing**
1. Apply the Namespace:
   ```bash
   kubectl apply -f namespace.yaml  # Creates the 'webapp' namespace
   ```
2. Verify:
   ```bash
   kubectl get namespaces  # Lists namespaces, should include 'webapp'
   kubectl describe namespace webapp  # Shows namespace details
   ```

### **Dependencies**
- None.

---

## **2️⃣ Pod**

### **Explanation**
- **Purpose**: The smallest deployable unit, running one or more containers that share storage and networking.
- **Use Case**: Running a single instance of the Flask app for testing before scaling with a Deployment.

### **YAML (`flask-pod.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Pods
kind: Pod                   # Defines the resource type as a Pod
metadata:                   # Metadata section for the Pod
  name: flask-pod           # Name of the Pod
  namespace: webapp         # Namespace where the Pod is created
  labels:                   # Labels for identifying the Pod
    app: flask-app          # Label for Service or NetworkPolicy selection
spec:                       # Specification for the Pod's desired state
  containers:               # List of containers in the Pod
  - name: flask-app         # Name of the container
    image: siva9989/employee-app:latest # Docker image for the Flask app
    ports:                  # Ports exposed by the container
    - containerPort: 5000   # Port 5000 for Flask
    env:                    # Environment variables for the Flask app
    - name: DB_HOST         # Database host
      value: "postgres-service" # Service name for PostgreSQL
    - name: DB_NAME         # Database name
      valueFrom:            # Source from Secret
        secretKeyRef:       # References a Secret key
          name: postgres-secret # Name of the Secret
          key: POSTGRES_DB   # Key for database name
    - name: DB_USER         # Database user
      valueFrom:            # Source from Secret
        secretKeyRef:       # References a Secret key
          name: postgres-secret # Name of the Secret
          key: POSTGRES_USER # Key for database user
    - name: DB_PASS         # Database password
      valueFrom:            # Source from Secret
        secretKeyRef:       # References a Secret key
          name: postgres-secret # Name of the Secret
          key: POSTGRES_PASSWORD # Key for database password
```

### **Usage**
- Runs a single Flask container, connecting to PostgreSQL via environment variables from a Secret.
- Used for initial testing before scaling with a Deployment.

### **Testing**
1. Apply the Secret, PostgreSQL Service, and Pod (PostgreSQL Service is defined later, but needed for connectivity):
   ```bash
   kubectl apply -f secret.yaml  # Creates the Secret (defined in Secret section)
   kubectl apply -f postgres-service.yaml  # Creates the PostgreSQL Service (defined later)
   kubectl apply -f flask-pod.yaml  # Creates the Flask Pod
   ```
2. Verify:
   ```bash
   kubectl get pods -n webapp  # Lists Pods, should show 'flask-pod' as Running
   kubectl describe pod flask-pod -n webapp  # Shows Pod details and events
   ```
3. Test:
   - Port-forward to access the Flask app:
     ```bash
     kubectl port-forward pod/flask-pod 8080:5000 -n webapp
     ```
     - Open `http://localhost:8080` in a browser or run:
       ```bash
       curl http://localhost:8080  # Should return Flask app response (e.g., employee app UI or API)
       ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`).
- PostgreSQL Service (`postgres-service`) for database connectivity.

---

## **3️⃣ Deployment**

### **Explanation**
- **Purpose**: Manages stateless applications by maintaining a specified number of Pod replicas, supporting scaling and rolling updates.
- **Use Case**: Running multiple instances of the Flask app for high availability and load balancing.

### **YAML (`flask-deployment.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
kind: Deployment            # Defines the resource type as a Deployment
metadata:                   # Metadata section for the Deployment
  name: flask-app           # Name of the Deployment
  namespace: webapp         # Namespace where the Deployment is created
spec:                       # Specification for the Deployment's desired state
  replicas: 2               # Number of Pod replicas (increased from 1 for example)
  selector:                 # Selector to match Pods managed by the Deployment
    matchLabels:            # Labels to match Pods
      app: flask-app        # Label key-value pair to identify Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this Deployment
      labels:               # Labels assigned to Pods
        app: flask-app      # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
      - name: flask-app     # Name of the container
        image: siva9989/employee-app:latest # Docker image for the Flask app
        ports:              # Ports exposed by the container
        - containerPort: 5000 # Port 5000 for Flask
        env:                # Environment variables for the Flask app
        - name: DB_HOST     # Database host
          value: "postgres-service" # Service name for PostgreSQL
        - name: DB_NAME     # Database name
          valueFrom:        # Source from Secret
            secretKeyRef:   # References a Secret key
              name: postgres-secret # Name of the Secret
              key: POSTGRES_DB # Key for database name
        - name: DB_USER     # Database user
          valueFrom:        # Source from Secret
            secretKeyRef:   # References a Secret key
              name: postgres-secret # Name of the Secret
              key: POSTGRES_USER # Key for database user
        - name: DB_PASS     # Database password
          valueFrom:        # Source from Secret
            secretKeyRef:   # References a Secret key
              name: postgres-secret # Name of the Secret
              key: POSTGRES_PASSWORD # Key for database password
```

### **Usage**
- Manages 2 Flask Pods, ensuring high availability and load balancing.
- Connects to PostgreSQL via the `postgres-service` Service and Secret credentials.

### **Testing**
1. Apply the Deployment:
   ```bash
   kubectl apply -f secret.yaml  # Ensures Secret is available
   kubectl apply -f postgres-service.yaml  # Ensures PostgreSQL Service is available
   kubectl apply -f flask-deployment.yaml  # Creates the Deployment
   ```
2. Verify:
   ```bash
   kubectl get deployments -n webapp  # Shows 'flask-app' with 2/2 replicas
   kubectl get pods -n webapp -l app=flask-app  # Lists 2 Flask Pods
   kubectl describe deployment flask-app -n webapp  # Shows Deployment details
   ```
3. Test:
   - Port-forward a Pod or use a Service (defined later):
     ```bash
     kubectl port-forward pod/<flask-pod-name> 8080:5000 -n webapp
     ```
     - Run `curl http://localhost:8080` to verify the Flask app response.
   - Scale the Deployment:
     ```bash
     kubectl scale deployment flask-app --replicas=3 -n webapp  # Scales to 3 replicas
     kubectl get pods -n webapp -l app=flask-app  # Confirms 3 Pods
     ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`).
- PostgreSQL Service (`postgres-service`).

---

## **4️⃣ StatefulSet**

### **Explanation**
- **Purpose**: Manages stateful applications with stable Pod identities, persistent storage, and ordered operations.
- **Use Case**: Running the PostgreSQL database with stable network identities and persistent data, replacing the provided Deployment for PostgreSQL.

### **YAML (`postgres-statefulset.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for StatefulSets
kind: StatefulSet           # Defines the resource type as a StatefulSet
metadata:                   # Metadata section for the StatefulSet
  name: postgres            # Name of the StatefulSet
  namespace: webapp         # Namespace where the StatefulSet is created
spec:                       # Specification for the StatefulSet's desired state
  serviceName: postgres-headless # Name of the headless Service for DNS resolution
  replicas: 1               # Number of Pod replicas
  selector:                 # Selector to match Pods managed by the StatefulSet
    matchLabels:            # Labels to match Pods
      app: postgres         # Label key-value pair to identify Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this StatefulSet
      labels:               # Labels assigned to Pods
        app: postgres       # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
      - name: postgres      # Name of the container
        image: postgres:14  # Docker image for PostgreSQL
        envFrom:            # Load environment variables from Secret
        - secretRef:        # References the Secret
            name: postgres-secret # Name of the Secret
        ports:              # Ports exposed by the container
        - containerPort: 5432 # Port 5432 for PostgreSQL
        volumeMounts:       # Mounts volumes into the container
        - name: postgres-data # Name of the volume
          mountPath: /var/lib/postgresql/data # Path for PostgreSQL data
  volumeClaimTemplates:     # Template for creating PVCs for each Pod
  - metadata:               # Metadata for the PVC
      name: postgres-data   # Name of the PVC (used in volumeMounts)
    spec:                   # Specification for the PVC
      accessModes: ["ReadWriteOnce"] # Requests read/write access by a single node
      resources:            # Resource requirements for the PVC
        requests:           # Specifies the minimum resources needed
          storage: 1Gi      # Requests 1 gibibyte of storage
      storageClassName: microk8s-hostpath # Storage class for MicroK8s
```

### **Usage**
- Runs a single PostgreSQL Pod with stable identity (`postgres-0`) and persistent storage.
- Uses a Headless Service for DNS-based access and a Secret for credentials.

### **Testing**
1. Apply the Headless Service, Secret, and StatefulSet:
   ```bash
   kubectl apply -f secret.yaml  # Ensures Secret is available
   kubectl apply -f postgres-headless-service.yaml  # Creates Headless Service (defined later)
   kubectl apply -f postgres-statefulset.yaml  # Creates the StatefulSet
   ```
2. Verify:
   ```bash
   kubectl get statefulsets -n webapp  # Shows 'postgres' with 1/1 replicas
   kubectl get pods -n webapp -l app=postgres  # Shows 'postgres-0'
   kubectl get pvc -n webapp  # Shows 'postgres-data-postgres-0'
   ```
3. Test:
   - Initialize the `employees` table:
     ```bash
     kubectl exec -it postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "CREATE TABLE employees (id SERIAL PRIMARY KEY, name TEXT, email TEXT, role TEXT);"
     ```
   - Insert test data:
     ```bash
     kubectl exec -it postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "INSERT INTO employees (name, email, role) VALUES ('John Doe', 'john@example.com', 'Developer');"
     ```
   - Verify data persistence:
     ```bash
     kubectl delete pod postgres-0 -n webapp  # Deletes Pod, StatefulSet recreates it
     kubectl exec -it postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"  # Shows 'John Doe' record
     ```
   - Test DNS via Headless Service:
     ```bash
     kubectl run -i --tty test-pod --image=busybox --rm --restart=Never -n webapp -- sh
     ```
     - Inside the Pod:
       ```bash
       nslookup postgres-0.postgres-headless.webapp.svc.cluster.local  # Resolves to Pod IP
       ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`).
- Headless Service (`postgres-headless`).
- MicroK8s `hostpath` storage class.

---

## **5️⃣ Service - ClusterIP**

### **Explanation**
- **Purpose**: Exposes Pods internally within the cluster using a stable virtual IP, enabling load balancing.
- **Use Case**: Allowing the Flask app to communicate with the PostgreSQL database internally.

### **YAML (`postgres-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: postgres-service    # Name of the Service
  namespace: webapp         # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  selector:                 # Selects Pods to route traffic to
    app: postgres           # Matches Pods with label "app: postgres"
  ports:                    # Ports exposed by the Service
  - protocol: TCP           # Protocol used (TCP)
    port: 5432              # Port exposed by the Service
    targetPort: 5432        # Port on the Pod to forward traffic to
  type: ClusterIP           # Service type (internal to the cluster)
```

### **Usage**
- Exposes the PostgreSQL Pod(s) at `postgres-service.webapp.svc.cluster.local:5432`.
- Used by the Flask app to connect to the database.

### **Testing**
1. Apply the Service (assuming PostgreSQL StatefulSet is running):
   ```bash
   kubectl apply -f postgres-service.yaml  # Creates the ClusterIP Service
   ```
2. Verify:
   ```bash
   kubectl get services -n webapp  # Shows 'postgres-service' with a ClusterIP
   kubectl describe service postgres-service -n webapp  # Shows Service details
   ```
3. Test:
   - From a Flask Pod (e.g., `flask-pod`):
     ```bash
     kubectl exec flask-pod -n webapp -- curl postgres-service:5432  # Should connect to PostgreSQL
     ```
   - Or create a test Pod:
     ```bash
     kubectl run -i --tty test-pod --image=busybox --rm --restart=Never -n webapp -- sh
     ```
     - Inside the Pod:
       ```bash
       wget -qO- postgres-service:5432  # Tests connectivity to PostgreSQL
       ```

### **Dependencies**
- Namespace (`webapp`).
- StatefulSet or Pod with `app: postgres` label.

---

## **6️⃣ Service - NodePort**

### **Explanation**
- **Purpose**: Exposes Pods on a specific port of each cluster node, allowing external access via `<node-ip>:<node-port>`.
- **Use Case**: Exposing the Flask app for external testing or access in a development environment.

### **YAML (`flask-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: flask-service       # Name of the Service
  namespace: webapp         # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  type: NodePort            # Service type (exposes on node ports)
  selector:                 # Selects Pods to route traffic to
    app: flask-app          # Matches Pods with label "app: flask-app"
  ports:                    # Ports exposed by the Service
  - protocol: TCP           # Protocol used (TCP)
    port: 80                # Port exposed by the Service
    targetPort: 5000        # Port on the Pod to forward traffic to
    nodePort: 30800         # Node port (30000-32767 range)
```

### **Usage**
- Exposes the Flask app on port 30800 of each cluster node.
- Allows external access via `<node-ip>:30800`.

### **Testing**
1. Apply the Service:
   ```bash
   kubectl apply -f flask-service.yaml  # Creates the NodePort Service
   ```
2. Verify:
   ```bash
   kubectl get services -n webapp  # Shows 'flask-service' with port 30800
   kubectl describe service flask-service -n webapp  # Shows Service details
   ```
3. Test:
   - Get the node IP (in MicroK8s, often the host IP):
     ```bash
     kubectl get nodes -o wide  # Shows node IPs
     ```
   - Access the Flask app:
     ```bash
     curl http://<node-ip>:30800  # Should return Flask app response
     ```
   - In MicroK8s, if running locally:
     ```bash
     curl http://localhost:30800  # Access via localhost
     ```

### **Dependencies**
- Namespace (`webapp`).
- Deployment or Pod with `app: flask-app` label.

---

## **7️⃣ Service - Headless**

### **Explanation**
- **Purpose**: Provides direct DNS-based access to individual Pods without a cluster IP, ideal for stateful applications.
- **Use Case**: Enabling stable DNS names for PostgreSQL Pods in the StatefulSet.

### **YAML (`postgres-headless-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: postgres-headless   # Name of the Service
  namespace: webapp         # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  selector:                 # Selects Pods to manage
    app: postgres           # Matches Pods with label "app: postgres"
  ports:                    # Ports exposed by the Service
  - protocol: TCP           # Protocol used (TCP)
    port: 5432              # Port exposed by the Service
    targetPort: 5432        # Port on the Pod to forward traffic to
  clusterIP: None           # Makes the Service headless (no cluster IP)
```

### **Usage**
- Provides DNS records like `postgres-0.postgres-headless.webapp.svc.cluster.local` for PostgreSQL Pods.
- Used by the StatefulSet for stable network identities.

### **Testing**
1. Apply the Headless Service:
   ```bash
   kubectl apply -f postgres-headless-service.yaml  # Creates the Headless Service
   ```
2. Verify:
   ```bash
   kubectl get services -n webapp  # Shows 'postgres-headless' with ClusterIP 'None'
   kubectl describe service postgres-headless -n webapp  # Shows Service details
   ```
3. Test (assuming PostgreSQL StatefulSet is running):
   - From a test Pod:
     ```bash
     kubectl run -i --tty test-pod --image=busybox --rm --restart=Never -n webapp -- sh
     ```
     - Inside the Pod:
       ```bash
       nslookup postgres-0.postgres-headless.webapp.svc.cluster.local  # Resolves to Pod IP
       wget -qO- postgres-0.postgres-headless.webapp.svc.cluster.local:5432  # Tests connectivity
       ```

### **Dependencies**
- Namespace (`webapp`).
- StatefulSet with `app: postgres` label.

---

## **8️⃣ Service - LoadBalancer**

### **Explanation**
- **Purpose**: Exposes Pods externally via a cloud provider’s load balancer or local solution (e.g., MetalLB), assigning an external IP.
- **Use Case**: Providing public access to the Flask app in production.

### **YAML (`flask-loadbalancer-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: flask-loadbalancer  # Name of the Service
  namespace: webapp         # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  type: LoadBalancer        # Service type (exposes externally via load balancer)
  selector:                 # Selects Pods to route traffic to
    app: flask-app          # Matches Pods with label "app: flask-app"
  ports:                    # Ports exposed by the Service
  - protocol: TCP           # Protocol used (TCP)
    port: 80                # Port exposed by the Service
    targetPort: 5000        # Port on the Pod to forward traffic to
```

### **Usage**
- Exposes the Flask app externally via an external IP.
- Suitable for production access, complementing the NodePort Service.

### **Testing**
1. Apply the Service:
   ```bash
   kubectl apply -f flask-loadbalancer-service.yaml  # Creates the LoadBalancer Service
   ```
2. Verify:
   ```bash
   kubectl get services -n webapp  # Shows 'flask-loadbalancer' with an external IP
   kubectl describe service flask-loadbalancer -n webapp  # Shows Service details
   ```
3. Test:
   - Enable MetalLB in MicroK8s:
     ```bash
     microk8s enable metallb:192.168.1.100-192.168.1.200  # Assigns IP range
     ```
   - Get the external IP:
     ```bash
     kubectl get svc flask-loadbalancer -n webapp -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
     ```
   - Access:
     ```bash
     curl http://<external-ip>  # Should return Flask app response
     ```

### **Dependencies**
- Namespace (`webapp`).
- Deployment or Pod with `app: flask-app` label.
- MetalLB or cloud provider for LoadBalancer support.

---

## **9️⃣ ConfigMap**

### **Explanation**
- **Purpose**: Stores non-sensitive configuration data as key-value pairs, decoupling configuration from code.
- **Use Case**: Providing configuration settings for the Flask app (e.g., app environment or log level).

### **YAML (`configmap.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for ConfigMaps
kind: ConfigMap             # Defines the resource type as a ConfigMap
metadata:                   # Metadata section for the ConfigMap
  name: flask-config        # Name of the ConfigMap
  namespace: webapp         # Namespace where the ConfigMap is created
data:                       # Key-value pairs for configuration data
  APP_ENV: "production"     # Application environment
  LOG_LEVEL: "debug"        # Logging level
```

### **Usage**
- Mounts configuration as environment variables in the Flask Pods or Deployment.
- Can also be used in PostgreSQL for non-sensitive settings.

### **Testing with Pod**
1. **YAML (`flask-pod-with-configmap.yaml`)**
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: flask-config-pod    # Name of the Pod
     namespace: webapp         # Namespace where the Pod is created
   spec:                       # Specification for the Pod's desired state
     containers:               # List of containers in the Pod
     - name: flask-app         # Name of the container
       image: siva9989/employee-app:latest # Docker image for the Flask app
       ports:                  # Ports exposed by the container
       - containerPort: 5000   # Port 5000 for Flask
       env:                    # Environment variables for the Flask app
       - name: APP_ENV         # Environment variable from ConfigMap
         valueFrom:            # Source from ConfigMap
           configMapKeyRef:    # References a ConfigMap key
             name: flask-config # Name of the ConfigMap
             key: APP_ENV     # Key for app environment
       - name: LOG_LEVEL       # Environment variable from ConfigMap
         valueFrom:            # Source from ConfigMap
           configMapKeyRef:    # References a ConfigMap key
             name: flask-config # Name of the ConfigMap
             key: LOG_LEVEL   # Key for log level
       - name: DB_HOST         # Database host (for completeness)
         value: "postgres-service"
       - name: DB_NAME         # Database name
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_DB
       - name: DB_USER         # Database user
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_USER
       - name: DB_PASS         # Database password
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_PASSWORD
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f configmap.yaml  # Creates the ConfigMap
   kubectl apply -f secret.yaml  # Ensures Secret is available
   kubectl apply -f postgres-service.yaml  # Ensures PostgreSQL Service is available
   kubectl apply -f flask-pod-with-configmap.yaml  # Creates the Pod
   ```
   - Verify:
     ```bash
     kubectl get configmaps -n webapp  # Shows 'flask-config'
     kubectl get pods -n webapp  # Shows 'flask-config-pod' as Running
     kubectl exec flask-config-pod -n webapp -- env  # Shows APP_ENV=production, LOG_LEVEL=debug
     ```

### **Testing with Deployment**
1. Update `flask-deployment.yaml`:
   ```yaml
   apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
   kind: Deployment            # Defines the resource type as a Deployment
   metadata:                   # Metadata section for the Deployment
     name: flask-app           # Name of the Deployment
     namespace: webapp         # Namespace where the Deployment is created
   spec:                       # Specification for the Deployment's desired state
     replicas: 2               # Number of Pod replicas
     selector:                 # Selector to match Pods managed by the Deployment
       matchLabels:            # Labels to match Pods
         app: flask-app        # Label key-value pair to identify Pods
     template:                 # Template for creating Pods
       metadata:               # Metadata for Pods created by this Deployment
         labels:               # Labels assigned to Pods
           app: flask-app      # Same label as in selector
       spec:                   # Specification for the Pods
         containers:           # List of containers in each Pod
         - name: flask-app     # Name of the container
           image: siva9989/employee-app:latest # Docker image for the Flask app
           ports:              # Ports exposed by the container
           - containerPort: 5000 # Port 5000 for Flask
           env:                # Environment variables for the Flask app
           - name: APP_ENV     # Environment variable from ConfigMap
             valueFrom:        # Source from ConfigMap
               configMapKeyRef:# References a ConfigMap key
                 name: flask-config # Name of the ConfigMap
                 key: APP_ENV   # Key for app environment
           - name: LOG_LEVEL   # Environment variable from ConfigMap
             valueFrom:        # Source from ConfigMap
               configMapKeyRef:# References a ConfigMap key
                 name: flask-config # Name of the ConfigMap
                 key: LOG_LEVEL # Key for log level
           - name: DB_HOST     # Database host
             value: "postgres-service"
           - name: DB_NAME     # Database name
             valueFrom:        # Source from Secret
               secretKeyRef:   # References a Secret key
                 name: postgres-secret # Name of the Secret
                 key: POSTGRES_DB
           - name: DB_USER     # Database user
             valueFrom:        # Source from Secret
               secretKeyRef:   # References a Secret key
                 name: postgres-secret # Name of the Secret
                 key: POSTGRES_USER
           - name: DB_PASS     # Database password
             valueFrom:        # Source from Secret
               secretKeyRef:   # References a Secret key
                 name: postgres-secret # Name of the Secret
                 key: POSTGRES_PASSWORD
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f flask-deployment.yaml  # Updates the Deployment
   kubectl get pods -n webapp -l app=flask-app  # Lists Deployment Pods
   kubectl exec <pod-name> -n webapp -- env  # Shows APP_ENV, LOG_LEVEL
   ```

### **Testing with StatefulSet**
- PostgreSQL StatefulSet could use ConfigMap for non-sensitive settings (e.g., `POSTGRES_LOGGING`), but the provided Secret is sufficient. Example:
  ```yaml
  env:
  - name: POSTGRES_LOGGING
    valueFrom:
      configMapKeyRef:
        name: flask-config
        key: LOG_LEVEL
  ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`) and PostgreSQL Service for Pod/Deployment.

---

## **10️⃣ Secret**

### **Explanation**
- **Purpose**: Stores sensitive data (e.g., passwords, API keys) in Base64-encoded format with access control.
- **Use Case**: Providing PostgreSQL credentials to both Flask and PostgreSQL containers.

### **YAML (`secret.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Secrets
kind: Secret                # Defines the resource type as a Secret
metadata:                   # Metadata section for the Secret
  name: postgres-secret     # Name of the Secret
  namespace: webapp         # Namespace where the Secret is created
type: Opaque                # Type of Secret (generic key-value pairs)
stringData:                 # Plaintext data (Kubernetes encodes to Base64)
  POSTGRES_DB: employee_db  # Database name
  POSTGRES_USER: employee_user # Database user
  POSTGRES_PASSWORD: secret123 # Database password
```

### **Usage**
- Provides credentials (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) to Flask and PostgreSQL.
- Mounted as environment variables in Flask Pods/Deployment and PostgreSQL StatefulSet.

### **Testing with Pod**
1. Use `flask-pod-with-configmap.yaml` (includes Secret) or create a minimal Pod:
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: flask-secret-pod    # Name of the Pod
     namespace: webapp         # Namespace where the Pod is created
   spec:                       # Specification for the Pod's desired state
     containers:               # List of containers in the Pod
     - name: flask-app         # Name of the container
       image: siva9989/employee-app:latest # Docker image for the Flask app
       command: ["sh", "-c", "env && sleep 3600"] # Prints env variables
       env:                    # Environment variables for the Flask app
       - name: DB_NAME         # Database name
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_DB
       - name: DB_USER         # Database user
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_USER
       - name: DB_PASS         # Database password
         valueFrom:            # Source from Secret
           secretKeyRef:       # References a Secret key
             name: postgres-secret # Name of the Secret
             key: POSTGRES_PASSWORD
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f secret.yaml  # Creates the Secret
   kubectl apply -f flask-secret-pod.yaml  # Creates the Pod
   kubectl get secrets -n webapp  # Shows 'postgres-secret'
   kubectl get pods -n webapp  # Shows 'flask-secret-pod'
   kubectl logs flask-secret-pod -n webapp  # Shows DB_NAME=employee_db, etc.
   ```

### **Testing with Deployment**
- Use the updated `flask-deployment.yaml` (includes Secret):
  ```bash
  kubectl apply -f flask-deployment.yaml
  kubectl exec <pod-name> -n webapp -- env  # Shows DB_NAME, DB_USER, DB_PASS
  ```

### **Testing with StatefulSet**
- The PostgreSQL StatefulSet uses the Secret via `envFrom`:
  ```bash
  kubectl apply -f postgres-statefulset.yaml
  kubectl exec postgres-0 -n webapp -- env  # Shows POSTGRES_DB=employee_db, etc.
  ```

### **Dependencies**
- Namespace (`webapp`).

---

## **11️⃣ Persistent Volume (PV)**

### **Explanation**
- **Purpose**: Represents a storage resource in the cluster, providing persistent storage for Pods.
- **Use Case**: Storing PostgreSQL data to persist beyond Pod restarts (alternative to ephemeral PVC).

### **YAML (`pv.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for PersistentVolumes
kind: PersistentVolume      # Defines the resource type as a PersistentVolume
metadata:                   # Metadata section for the PV
  name: my-pv               # Name of the PersistentVolume
spec:                       # Specification for the PV's desired state
  capacity:                 # Storage capacity
    storage: 1Gi            # 1 Gibibyte of storage
  accessModes:              # Access modes for the volume
    - ReadWriteOnce         # Can be mounted as read-write by one node
  hostPath:                 # Type of storage (local host path for MicroK8s)
    path: "/mnt/data"       # Path on the host node
```

### **Usage**
- Provides storage for a PVC, which the PostgreSQL StatefulSet can use instead of the ephemeral PVC.
- Ensures data persistence for the database.

### **Testing**
1. Apply the PV:
   ```bash
   kubectl apply -f pv.yaml  # Creates the PV
   ```
2. Verify:
   ```bash
   kubectl get pv  # Shows 'my-pv' as 'Available'
   kubectl describe pv my-pv  # Shows PV details
   ```
3. Testing requires a PVC (next section).

### **Dependencies**
- None (PV is cluster-wide).

---

## **12️⃣ PersistentVolumeClaim (PVC)**

### **Explanation**
- **Purpose**: Requests storage from a PV or dynamic provisioner, binding to a PV for use by Pods.
- **Use Case**: Providing persistent storage for PostgreSQL, either via the provided PV or the StatefulSet’s ephemeral PVC.

### **YAML (`pvc.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for PersistentVolumeClaims
kind: PersistentVolumeClaim # Defines the resource type as a PersistentVolumeClaim
metadata:                   # Metadata section for the PVC
  name: my-pvc              # Name of the PersistentVolumeClaim
  namespace: webapp         # Namespace where the PVC is created
spec:                       # Specification for the PVC's desired state
  accessModes:              # Requested access modes
  - ReadWriteOnce           # Requests read/write access by a single node
  resources:                # Resource requirements for the PVC
    requests:               # Specifies the minimum resources needed
      storage: 1Gi          # Requests 1 gibibyte of storage
```

### **Testing with Pod**
1. **YAML (`flask-pod-with-pvc.yaml`)**
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: flask-pvc-pod       # Name of the Pod
     namespace: webapp         # Namespace where the Pod is created
     labels:                   # Labels for NetworkPolicy
       app: flask-pvc          # Label for identification
   spec:                       # Specification for the Pod's desired state
     volumes:                  # List of volumes available to the Pod
     - name: storage           # Name of the volume
       persistentVolumeClaim:  # Links to a PersistentVolumeClaim
         claimName: my-pvc     # Name of the PVC
     containers:               # List of containers in the Pod
     - name: flask-app         # Name of the container
       image: siva9989/employee-app:latest # Docker image for the Flask app
       command: ["sh", "-c", "echo 'Test data' > /mnt/storage/data.txt && sleep 3600"] # Writes data
       volumeMounts:           # Mounts the volume into the container
       - mountPath: "/mnt/storage" # Path where the volume is mounted
         name: storage         # Name of the volume
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f pv.yaml  # Creates the PV
   kubectl apply -f pvc.yaml  # Creates the PVC
   kubectl apply -f flask-pod-with-pvc.yaml  # Creates the Pod
   kubectl get pv  # Shows 'my-pv' as 'Bound'
   kubectl get pvc -n webapp  # Shows 'my-pvc' as 'Bound'
   kubectl exec flask-pvc-pod -n webapp -- cat /mnt/storage/data.txt  # Shows 'Test data'
   ```
   - Test persistence:
     ```bash
     kubectl delete pod flask-pvc-pod -n webapp
     kubectl apply -f flask-pod-with-pvc.yaml
     kubectl exec flask-pvc-pod -n webapp -- cat /mnt/storage/data.txt  # Data persists
     ```

### **Testing with Deployment**
1. **YAML (`flask-deployment-with-pvc.yaml`)**
   ```yaml
   apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
   kind: Deployment            # Defines the resource type as a Deployment
   metadata:                   # Metadata section for the Deployment
     name: flask-pvc-deployment # Name of the Deployment
     namespace: webapp         # Namespace where the Deployment is created
   spec:                       # Specification for the Deployment's desired state
     replicas: 1               # Single replica (ReadWriteOnce limitation)
     selector:                 # Selector to match Pods managed by the Deployment
       matchLabels:            # Labels to match Pods
         app: flask-pvc        # Label key-value pair
     template:                 # Template for creating Pods
       metadata:               # Metadata for Pods created by this Deployment
         labels:               # Labels assigned to Pods
           app: flask-pvc      # Same label as in selector
       spec:                   # Specification for the Pods
         volumes:              # List of volumes available to the Pod
         - name: storage       # Name of the volume
           persistentVolumeClaim: # Links to a PersistentVolumeClaim
             claimName: my-pvc # Name of the PVC
         containers:           # List of containers in each Pod
         - name: flask-app     # Name of the container
           image: siva9989/employee-app:latest # Docker image
           command: ["sh", "-c", "echo 'Test data' > /mnt/storage/data.txt && sleep 3600"]
           volumeMounts:       # Mounts the volume into the container
           - mountPath: "/mnt/storage" # Path where the volume is mounted
             name: storage     # Name of the volume
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f flask-deployment-with-pvc.yaml
   kubectl get pods -n webapp -l app=flask-pvc
   kubectl exec <pod-name> -n webapp -- cat /mnt/storage/data.txt  # Shows 'Test data'
   ```

### **Testing with StatefulSet**
- The PostgreSQL StatefulSet uses an ephemeral PVC (`postgres-data`). To use `my-pvc`:
  ```yaml
  spec:
    volumeClaimTemplates: []
    volumes:
    - name: postgres-data
      persistentVolumeClaim:
        claimName: my-pvc
  ```
- Apply and Test:
  ```bash
  kubectl apply -f postgres-statefulset.yaml
  kubectl exec postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"  # Data persists
  ```

### **Dependencies**
- Namespace (`webapp`).
- PV (`my-pv`) for binding.

---

## **13️⃣ Job**

### **Explanation**
- **Purpose**: Runs a task to completion, creating Pods that terminate once done.
- **Use Case**: Initializing the PostgreSQL `employees` table with schema and data.

### **YAML (`db-init-job.yaml`)**
```yaml
apiVersion: batch/v1        # Specifies the Kubernetes API version for Jobs
kind: Job                   # Defines the resource type as a Job
metadata:                   # Metadata section for the Job
  name: db-init-job         # Name of the Job
  namespace: webapp         # Namespace where the Job is created
spec:                       # Specification for the Job's desired state
  completions: 1            # Number of successful completions required
  parallelism: 1            # Number of Pods to run in parallel
  template:                 # Template for creating Pods
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
      - name: db-init       # Name of the container
        image: postgres:14  # Docker image for PostgreSQL client
        command: ["psql", "-h", "postgres-service", "-U", "employee_user", "-d", "employee_db", "-c", "CREATE TABLE IF NOT EXISTS employees (id SERIAL PRIMARY KEY, name TEXT, email TEXT, role TEXT); INSERT INTO employees (name, email, role) VALUES ('Jane Doe', 'jane@example.com', 'Manager') ON CONFLICT DO NOTHING;"]
        env:                # Environment variables for the container
        - name: PGPASSWORD  # Password for psql
          valueFrom:        # Source from Secret
            secretKeyRef:   # References a Secret key
              name: postgres-secret # Name of the Secret
              key: POSTGRES_PASSWORD
      restartPolicy: Never # Ensures the Pod does not restart
```

### **Usage**
- Creates the `employees` table and inserts a sample record.
- Runs once and terminates.

### **Testing**
1. Apply the Job:
   ```bash
   kubectl apply -f secret.yaml  # Ensures Secret is available
   kubectl apply -f postgres-service.yaml  # Ensures PostgreSQL Service is available
   kubectl apply -f db-init-job.yaml  # Creates the Job
   ```
2. Verify:
   ```bash
   kubectl get jobs -n webapp  # Shows 'db-init-job'
   kubectl get pods -n webapp  # Shows Job Pod as Completed
   ```
3. Test:
   ```bash
   kubectl logs <job-pod-name> -n webapp  # Shows psql output
   kubectl exec postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"  # Shows 'Jane Doe' record
   ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`).
- PostgreSQL Service (`postgres-service`) and StatefulSet.

---

## **14️⃣ CronJob**

### **Explanation**
- **Purpose**: Schedules Jobs to run at specified times or intervals, like a cron scheduler.
- **Use Case**: Periodically backing up the PostgreSQL database.

### **YAML (`db-backup-cronjob.yaml`)**
```yaml
apiVersion: batch/v1        # Specifies the Kubernetes API version for CronJobs
kind: CronJob               # Defines the resource type as a CronJob
metadata:                   # Metadata section for the CronJob
  name: db-backup-cronjob   # Name of the CronJob
  namespace: webapp         # Namespace where the CronJob is created
spec:                       # Specification for the CronJob's desired state
  schedule: "0 2 * * *"     # Runs daily at 2 AM
  jobTemplate:              # Template for Jobs created by the CronJob
    spec:                   # Specification for the Jobs
      template:             # Template for creating Pods
        spec:               # Specification for the Pods
          containers:       # List of containers in each Pod
          - name: db-backup # Name of the container
            image: postgres:14 # Docker image for PostgreSQL client
            command: ["sh", "-c", "pg_dump -h postgres-service -U employee_user employee_db > /backup/db_backup_$(date +%F).sql"]
            env:            # Environment variables for the container
            - name: PGPASSWORD # Password for pg_dump
              valueFrom:    # Source from Secret
                secretKeyRef: # References a Secret key
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
            volumeMounts:   # Mounts volume for backup storage
            - name: backup  # Name of the volume
              mountPath: /backup # Path for backup files
          restartPolicy: OnFailure # Restarts on failure
          volumes:          # Volumes for the Pod
          - name: backup    # Name of the volume
            emptyDir: {}    # Temporary storage for backups
```

### **Usage**
- Schedules a daily backup of the `employee_db` database.
- Stores backups temporarily (for simplicity; production would use persistent storage).

### **Testing**
1. Apply the CronJob:
   ```bash
   kubectl apply -f db-backup-cronjob.yaml
   ```
2. Verify:
   ```bash
   kubectl get cronjobs -n webapp  # Shows 'db-backup-cronjob'
   ```
3. Test:
   - Trigger a manual Job:
     ```bash
     kubectl create job --from=cronjob/db-backup-cronjob manual-backup -n webapp
     ```
   - Check the backup:
     ```bash
     kubectl get pods -n webapp  # Shows Job Pod
     kubectl exec <job-pod-name> -n webapp -- cat /backup/db_backup_$(date +%F).sql  # Shows SQL dump
     ```

### **Dependencies**
- Namespace (`webapp`).
- Secret (`postgres-secret`).
- PostgreSQL Service (`postgres-service`) and StatefulSet.

---

## **15️⃣ DaemonSet**

### **Explanation**
- **Purpose**: Ensures a Pod runs on every node (or a subset) in the cluster, typically for cluster-wide services.
- **Use Case**: Running a monitoring agent (e.g., Fluentd) to collect logs from Flask and PostgreSQL Pods.

### **YAML (`monitoring-daemonset.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for DaemonSets
kind: DaemonSet             # Defines the resource type as a DaemonSet
metadata:                   # Metadata section for the DaemonSet
  name: monitoring-agent    # Name of the DaemonSet
  namespace: webapp         # Namespace where the DaemonSet is created
spec:                       # Specification for the DaemonSet's desired state
  selector:                 # Selector to match Pods managed by the DaemonSet
    matchLabels:            # Labels to match Pods
      app: monitoring       # Label key-value pair
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this DaemonSet
      labels:               # Labels assigned to Pods
        app: monitoring     # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
      - name: fluentd       # Name of the container
        image: fluent/fluentd # Docker image for Fluentd
        resources:          # Resource limits for the container
          limits:           # Maximum resources
            memory: "200Mi" # Memory limit
          requests:         # Minimum resources
            memory: "100Mi" # Memory request
        volumeMounts:       # Mounts host logs for collection
        - name: logs        # Name of the volume
          mountPath: /fluentd/log # Path for log collection
      volumes:              # Volumes for the Pod
      - name: logs          # Name of the volume
        hostPath:           # Host path for container logs
          path: /var/log/containers # Path on the host
```

### **Usage**
- Runs Fluentd on every node to collect logs from Flask and PostgreSQL Pods.
- Enhances monitoring of the application.

### **Testing**
1. Apply the DaemonSet:
   ```bash
   kubectl apply -f monitoring-daemonset.yaml
   ```
2. Verify:
   ```bash
   kubectl get daemonsets -n webapp  # Shows 'monitoring-agent'
   kubectl get pods -n webapp -l app=monitoring -o wide  # Shows Pods on each node
   ```
3. Test:
   ```bash
   kubectl logs <fluentd-pod-name> -n webapp  # Shows Fluentd log collection output
   ```

### **Dependencies**
- Namespace (`webapp`).

---

## **16️⃣ Ingress**

### **Explanation**
- **Purpose**: Routes external HTTP/HTTPS traffic to Services based on URL paths or hostnames using an Ingress controller.
- **Use Case**: Exposing the Flask app at a custom domain (e.g., `employee-app.local`).

### **YAML (`flask-ingress.yaml`)**
```yaml
apiVersion: networking.k8s.io/v1 # Specifies the Kubernetes API version for Ingress
kind: Ingress                    # Defines the resource type as an Ingress
metadata:                        # Metadata section for the Ingress
  name: flask-ingress            # Name of the Ingress
  namespace: webapp              # Namespace where the Ingress is created
spec:                            # Specification for the Ingress's desired state
  rules:                         # Routing rules for the Ingress
  - host: employee-app.local     # Domain name for the Flask app
    http:                        # HTTP-specific configuration
      paths:                     # Paths to route traffic
      - path: /                  # Root path
        pathType: Prefix         # Matches any path starting with "/"
        backend:                 # Destination for traffic
          service:               # Links to a Service
            name: flask-service  # Name of the NodePort Service
            port:                # Port on the Service
              number: 80         # Port 80
```

### **Usage**
- Routes `http://employee-app.local/` to the `flask-service` Service.
- Provides a clean URL for accessing the Flask app.

### **Testing**
1. Apply the Ingress:
   ```bash
   kubectl apply -f flask-ingress.yaml
   ```
2. Verify:
   ```bash
   kubectl get ingress -n webapp  # Shows 'flask-ingress'
   kubectl describe ingress flask-ingress -n webapp  # Shows Ingress details
   ```
3. Test:
   - Enable Ingress in MicroK8s:
     ```bash
     microk8s enable ingress
     ```
   - Get the Ingress IP:
     ```bash
     kubectl get ingress -n webapp -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'
     ```
   - Update `/etc/hosts`:
     ```bash
     echo "<ingress-ip> employee-app.local" | sudo tee -a /etc/hosts
     ```
   - Access:
     ```bash
     curl http://employee-app.local  # Should return Flask app response
     ```

### **Dependencies**
- Namespace (`webapp`).
- Service (`flask-service`).
- Ingress controller.

---

## **17️⃣ RBAC - Role and RoleBinding**

### **Explanation**
- **Purpose**: Controls access to Kubernetes resources based on user or service account roles, enforcing security.
- **Use Case**: Allowing a developer (`student`) to view Pods in the `webapp` namespace but not modify them.

### **YAML (`rbac.yaml`)**
```yaml
apiVersion: rbac.authorization.k8s.io/v1 # Specifies the Kubernetes API version for RBAC
kind: Role                        # Defines the resource type as a Role
metadata:                         # Metadata section for the Role
  name: pod-reader                # Name of the Role
  namespace: webapp               # Namespace where the Role applies
rules:                            # Rules defining permissions
- apiGroups: [""]                 # Core API group (for Pods)
  resources: ["pods"]             # Resource type (Pods)
  verbs: ["get", "list", "watch"] # Allowed actions on Pods

---
apiVersion: rbac.authorization.k8s.io/v1 # Specifies the Kubernetes API version for RBAC
kind: RoleBinding                 # Defines the resource type as a RoleBinding
metadata:                         # Metadata section for the RoleBinding
  name: pod-reader-binding        # Name of the RoleBinding
  namespace: webapp               # Namespace where the RoleBinding applies
subjects:                         # Subjects granted the Role
- kind: User                      # Type of subject (User)
  name: student                   # Name of the user
  apiGroup: rbac.authorization.k8s.io # API group for RBAC subjects
roleRef:                          # Reference to the Role
  kind: Role                      # Type of resource being referenced
  name: pod-reader                # Name of the Role
  apiGroup: rbac.authorization.k8s.io # API group for RBAC roles
```

### **Usage**
- Grants `student` read-only access to Pods in `webapp`.
- Enhances security by limiting user permissions.

### **Testing**
1. Apply the RBAC:
   ```bash
   kubectl apply -f rbac.yaml
   ```
2. Verify:
   ```bash
   kubectl get role,rolebinding -n webapp
   kubectl describe role pod-reader -n webapp
   ```
3. Test:
   - Configure `kubectl` for `student` (requires admin to set up user credentials). Alternatively, use a service account:
     ```yaml
     apiVersion: v1
     kind: ServiceAccount
     metadata:
       name: test-sa
       namespace: webapp
     ---
     apiVersion: rbac.authorization.k8s.io/v1
     kind: RoleBinding
     metadata:
       name: pod-reader-sa-binding
       namespace: webapp
     subjects:
     - kind: ServiceAccount
       name: test-sa
       namespace: webapp
     roleRef:
       kind: Role
       name: pod-reader
       apiGroup: rbac.authorization.k8s.io
     ```
     ```bash
     kubectl apply -f sa.yaml
     kubectl apply -f sa-rolebinding.yaml
     kubectl auth can-i get pods --as=system:serviceaccount:webapp:test-sa -n webapp  # Returns 'yes'
     kubectl auth can-i delete pods --as=system:serviceaccount:webapp:test-sa -n webapp  # Returns 'no'
     ```

### **Dependencies**
- Namespace (`webapp`).

---

## **18️⃣ NetworkPolicy**

### **Explanation**
- **Purpose**: Defines rules for network traffic to and from Pods, enhancing security by restricting communication.
- **Use Case**: Allowing only the Flask app to communicate with the PostgreSQL Service.

### **YAML (`networkpolicy.yaml`)**
```yaml
apiVersion: networking.k8s.io/v1 # Specifies the Kubernetes API version for NetworkPolicies
kind: NetworkPolicy              # Defines the resource type as a NetworkPolicy
metadata:                        # Metadata section for the NetworkPolicy
  name: allow-flask-to-postgres  # Name of the NetworkPolicy
  namespace: webapp              # Namespace where the NetworkPolicy applies
spec:                            # Specification for the NetworkPolicy's desired state
  podSelector:                   # Selects Pods to which this policy applies
    matchLabels:                 # Labels to match Pods
      app: postgres              # Applies to PostgreSQL Pods
  policyTypes:                   # Types of traffic controlled
  - Ingress                      # Controls incoming traffic
  ingress:                       # Rules for incoming traffic
  - from:                        # Sources allowed to send traffic
    - podSelector:               # Selects source Pods
        matchLabels:             # Labels to match source Pods
          app: flask-app         # Allows traffic from Flask Pods
    ports:                     # Ports allowed for incoming traffic
    - protocol: TCP            # Protocol (TCP)
      port: 5432               # Port 5432 (PostgreSQL)
```

### **Usage**
- Restricts PostgreSQL access to only Flask Pods with `app: flask-app`.
- Enhances database security.

### **Testing**
1. Apply the NetworkPolicy:
   ```bash
   kubectl apply -f networkpolicy.yaml
   ```
2. Verify:
   ```bash
   kubectl get networkpolicies -n webapp
   kubectl describe networkpolicy allow-flask-to-postgres -n webapp
   ```
3. Test:
   - From a Flask Pod (allowed):
     ```bash
     kubectl exec <flask-pod-name> -n webapp -- curl postgres-service:5432  # Should connect
     ```
   - From a test Pod (denied):
     ```yaml
     apiVersion: v1
     kind: Pod
     metadata:
       name: test-pod
       namespace: webapp
     spec:
       containers:
       - name: busybox
         image: busybox
         command: ["sleep", "3600"]
     ```
     ```bash
     kubectl apply -f test-pod.yaml
     kubectl exec test-pod -n webapp -- wget -qO- postgres-service:5432  # Should timeout
     kubectl delete pod test-pod -n webapp
     ```

### **Dependencies**
- Namespace (`webapp`).
- StatefulSet with `app: postgres` label.
- Deployment or Pod with `app: flask-app` label.
- Network plugin (e.g., Calico).

---

## **End-to-End Flow**

### **Deployment and Testing Sequence**
1. **Namespace**:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl get namespaces
   ```
2. **RBAC**:
   ```bash
   kubectl apply -f rbac.yaml
   kubectl get role,rolebinding -n webapp
   ```
3. **ConfigMap**:
   ```bash
   kubectl apply -f configmap.yaml
   kubectl apply -f flask-pod-with-configmap.yaml
   kubectl exec flask-config-pod -n webapp -- env
   kubectl apply -f flask-deployment.yaml  # With ConfigMap
   ```
4. **Secret**:
   ```bash
   kubectl apply -f secret.yaml
   kubectl apply -f flask-secret-pod.yaml
   kubectl logs flask-secret-pod -n webapp
   ```
5. **PV and PVC**:
   ```bash
   kubectl apply -f pv.yaml
   kubectl apply -f pvc.yaml
   kubectl apply -f flask-pod-with-pvc.yaml
   kubectl exec flask-pvc-pod -n webapp -- cat /mnt/storage/data.txt
   kubectl apply -f flask-deployment-with-pvc.yaml
   ```
6. **Pod**:
   ```bash
   kubectl apply -f flask-pod.yaml
   kubectl port-forward pod/flask-pod 8080:5000 -n webapp
   curl http://localhost:8080
   ```
7. **Deployment**:
   ```bash
   kubectl apply -f flask-deployment.yaml
   kubectl get pods -n webapp -l app=flask-app
   ```
8. **Service - ClusterIP**:
   ```bash
   kubectl apply -f postgres-service.yaml
   kubectl exec flask-pod -n webapp -- curl postgres-service:5432
   ```
9. **Service - NodePort**:
   ```bash
   kubectl apply -f flask-service.yaml
   curl http://<node-ip>:30800
   ```
10. **Service - LoadBalancer**:
    ```bash
    kubectl apply -f flask-loadbalancer-service.yaml
    curl http://<external-ip>
    ```
11. **Service - Headless**:
    ```bash
    kubectl apply -f postgres-headless-service.yaml
    kubectl run -i --tty test-pod --image=busybox --rm -n webapp -- nslookup postgres-0.postgres-headless.webapp.svc.cluster.local
    ```
12. **StatefulSet**:
    ```bash
    kubectl apply -f postgres-statefulset.yaml
    kubectl exec postgres-0 -n webapp -- psql -U employee_user -d employee_db -c "SELECT * FROM employees;"
    ```
13. **Job**:
    ```bash
    kubectl apply -f db-init-job.yaml
    kubectl logs <job-pod-name> -n webapp
    ```
14. **CronJob**:
    ```bash
    kubectl apply -f db-backup-cronjob.yaml
    kubectl create job --from=cronjob/db-backup-cronjob manual-backup -n webapp
    ```
15. **DaemonSet**:
    ```bash
    kubectl apply -f monitoring-daemonset.yaml
    kubectl get pods -n webapp -l app=monitoring -o wide
    ```
16. **NetworkPolicy**:
    ```bash
    kubectl apply -f networkpolicy.yaml
    kubectl exec <flask-pod-name> -n webapp -- curl postgres-service:5432
    ```
17. **Ingress**:
    ```bash
    kubectl apply -f flask-ingress.yaml
    curl http://employee-app.local
    ```

### **Cleanup**
```bash
kubectl delete namespace webapp  # Deletes all resources
```

---

## **Summary**
This cheat sheet uses the Flask-PostgreSQL application to teach Kubernetes concepts, providing:
- **Tailored Explanations**: Each component’s role in the app (e.g., Secret for credentials).
- **Commented Configurations**: YAMLs adapted from your example, with additions for missing components.
- **Usage and Testing**: Practical steps to use and verify each component, centered on the Flask app and database.
- **End-to-End Flow**: Logical deployment sequence, ensuring students can follow and test incrementally.
- **MicroK8s Compatibility**: Uses `microk8s-hostpath` and add-ons for your environment.

The modular, example-driven approach makes it ideal for students to learn Kubernetes hands-on. 🚀