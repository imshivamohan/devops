# Complete Kubernetes Cheat Sheet for Students 🚀

This cheat sheet is designed for students learning Kubernetes, providing simple, commented YAML configurations for all major components: Namespace, Pod, Deployment, Services (ClusterIP, Headless, LoadBalancer), ConfigMap, Secret, Persistent Volume (PV), PersistentVolumeClaim (PVC), Job, CronJob, StatefulSet, Ingress, RBAC (Role and RoleBinding), DaemonSet, and NetworkPolicy. Each component includes:

- **Explanation**: Purpose and use case.
- **YAML Configuration**: Simple example with inline comments.
- **Usage**: How to integrate the component (e.g., mounting ConfigMap/Secret in Pods, Deployments, StatefulSets).
- **Testing**: Step-by-step commands to verify functionality, often with related resources (e.g., PVC with Pod, Deployment, StatefulSet).
- **Dependencies**: Any required resources for the component or tests.

The **End-to-End Flow** summarizes the deployment and testing order, ensuring a logical learning progression. All resources are scoped to the `kube-learn` namespace for isolation, and configurations are tailored for a MicroK8s environment using `hostPath` for simplicity.

---

## **Prerequisites**
- A running Kubernetes cluster (e.g., MicroK8s on Ubuntu, as per your preference).
- `kubectl` installed and configured.
- An Ingress controller (e.g., Nginx Ingress) for Ingress testing.
- A network plugin supporting NetworkPolicy (e.g., Calico) for NetworkPolicy testing.
- A user or service account (e.g., `student`) for RBAC testing.
- A cloud provider or local solution (e.g., MetalLB) for LoadBalancer testing.
- Basic familiarity with `kubectl` commands.

---

## **1️⃣ Namespace**

### **Explanation**
- **Purpose**: A Namespace isolates resources within a cluster, preventing naming conflicts and enabling multi-tenancy or environment separation (e.g., dev, prod).
- **Use Case**: Organizing resources for a project or team.

### **YAML (`namespace.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Namespaces
kind: Namespace             # Defines the resource type as a Namespace
metadata:                   # Metadata section for the resource
  name: kube-learn          # Name of the namespace for learning
```

### **Usage**
- Creates a namespace to scope all subsequent resources.
- All components below are applied in the `kube-learn` namespace.

### **Testing**
1. Apply the Namespace:
   ```bash
   kubectl apply -f namespace.yaml  # Creates the 'kube-learn' namespace
   ```
2. Verify the Namespace:
   ```bash
   kubectl get namespaces  # Lists all namespaces, should include 'kube-learn'
   kubectl describe namespace kube-learn  # Shows details of the namespace
   ```

### **Dependencies**
- None.

---

## **2️⃣ Pod**

### **Explanation**
- **Purpose**: The smallest deployable unit, running one or more containers that share storage and networking.
- **Use Case**: Running a single application instance for testing or simple workloads.

### **YAML (`pod.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Pods
kind: Pod                   # Defines the resource type as a Pod
metadata:                   # Metadata section for the Pod
  name: nginx-pod           # Name of the Pod
  namespace: kube-learn     # Namespace where the Pod is created
  labels:                   # Labels for identifying the Pod
    app: nginx              # Label for Service or NetworkPolicy selection
spec:                       # Specification for the Pod's desired state
  containers:               # List of containers in the Pod
    - name: nginx           # Name of the container
      image: nginx:latest   # Docker image to use (Nginx web server, latest version)
      ports:                # Ports exposed by the container
        - containerPort: 80 # Port 80 (HTTP) for the container
```

### **Usage**
- Runs a single Nginx container, exposing port 80.
- Can be accessed directly via `kubectl port-forward` or through a Service.

### **Testing**
1. Apply the Pod:
   ```bash
   kubectl apply -f pod.yaml  # Creates the Nginx Pod
   ```
2. Verify the Pod:
   ```bash
   kubectl get pods -n kube-learn  # Lists Pods, should show 'nginx-pod' as Running
   kubectl describe pod nginx-pod -n kube-learn  # Shows Pod details and events
   ```
3. Test the Pod:
   ```bash
   kubectl port-forward pod/nginx-pod 8080:80 -n kube-learn  # Forwards Pod's port 80 to localhost:8080
   ```
   - Open a browser or run `curl http://localhost:8080` to see the Nginx welcome page.

### **Dependencies**
- Namespace (`kube-learn`).

---

## **3️⃣ Service - ClusterIP**

### **Explanation**
- **Purpose**: Exposes a set of Pods internally within the cluster using a stable virtual IP, enabling load balancing.
- **Use Case**: Internal communication between microservices.

### **YAML (`clusterip-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: nginx-clusterip     # Name of the Service
  namespace: kube-learn     # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  selector:                 # Selects Pods to route traffic to
    app: nginx              # Matches Pods with label "app: nginx"
  ports:                    # Ports exposed by the Service
    - protocol: TCP         # Protocol used (TCP)
      port: 80              # Port exposed by the Service
      targetPort: 80        # Port on the Pod to forward traffic to
  type: ClusterIP           # Service type (internal to the cluster)
```

### **Usage**
- Exposes the `nginx-pod` (or later, Deployment Pods) internally at a cluster IP.
- Pods within the cluster can access it via `nginx-clusterip.kube-learn.svc.cluster.local:80`.

### **Testing**
1. Apply the Service (assuming `nginx-pod` is running):
   ```bash
   kubectl apply -f clusterip-service.yaml  # Creates the ClusterIP Service
   ```
2. Verify the Service:
   ```bash
   kubectl get services -n kube-learn  # Lists Services, shows 'nginx-clusterip' with a ClusterIP
   kubectl describe service nginx-clusterip -n kube-learn  # Shows Service details and endpoints
   ```
3. Test the Service:
   - Create a temporary Pod to test connectivity:
     ```bash
     kubectl run -i --tty test-pod --image=busybox --rm --restart=Never -n kube-learn -- sh
     ```
     - Inside the Pod, run:
       ```bash
       wget -qO- http://nginx-clusterip:80  # Accesses the Service, should return Nginx HTML
       ```
   - Alternatively, port-forward the Service:
     ```bash
     kubectl port-forward svc/nginx-clusterip 8080:80 -n kube-learn
     ```
     - Run `curl http://localhost:8080` to see the Nginx page.

### **Dependencies**
- Namespace (`kube-learn`).
- Pod (`nginx-pod`) or Deployment with `app: nginx` label.

---

## **4️⃣ Deployment**

### **Explanation**
- **Purpose**: Manages stateless applications by maintaining a specified number of Pod replicas, supporting scaling and rolling updates.
- **Use Case**: Deploying web servers or APIs where instances are interchangeable.

### **YAML (`deployment.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
kind: Deployment            # Defines the resource type as a Deployment
metadata:                   # Metadata section for the Deployment
  name: nginx-deployment    # Name of the Deployment
  namespace: kube-learn     # Namespace where the Deployment is created
spec:                       # Specification for the Deployment's desired state
  replicas: 3               # Number of Pod replicas to maintain
  selector:                 # Selector to match Pods managed by the Deployment
    matchLabels:            # Labels to match Pods
      app: nginx            # Label key-value pair to identify Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this Deployment
      labels:               # Labels assigned to Pods
        app: nginx          # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
        - name: nginx       # Name of the container
          image: nginx:latest # Docker image to use (Nginx web server, latest version)
          ports:             # Ports exposed by the container
            - containerPort: 80 # Port 80 (HTTP) for the container
```

### **Usage**
- Creates and manages 3 Nginx Pods, accessible via the existing `nginx-clusterip` Service.
- Supports scaling and updates (e.g., changing the image version).

### **Testing**
1. Apply the Deployment:
   ```bash
   kubectl apply -f deployment.yaml  # Creates the Deployment with 3 replicas
   ```
2. Verify the Deployment:
   ```bash
   kubectl get deployments -n kube-learn  # Lists Deployments, shows 'nginx-deployment' with 3/3 replicas
   kubectl get pods -n kube-learn -l app=nginx  # Lists Deployment Pods
   kubectl describe deployment nginx-deployment -n kube-learn  # Shows Deployment details
   ```
3. Test the Deployment via the Service:
   - Ensure `nginx-clusterip` Service is running (from step 3).
   - Port-forward the Service:
     ```bash
     kubectl port-forward svc/nginx-clusterip 8080:80 -n kube-learn
     ```
     - Run `curl http://localhost:8080` to verify Nginx response.
   - Scale the Deployment and test load balancing:
     ```bash
     kubectl scale deployment nginx-deployment --replicas=5 -n kube-learn  # Scales to 5 replicas
     kubectl get pods -n kube-learn -l app=nginx  # Confirms 5 Pods
     ```
     - Repeat `curl http://localhost:8080` multiple times to see load balancing across Pods.

### **Dependencies**
- Namespace (`kube-learn`).
- Service (`nginx-clusterip`) for testing access.

---

## **5️⃣ Service - Headless**

### **Explanation**
- **Purpose**: Provides direct DNS-based access to individual Pods without a cluster IP, ideal for stateful applications requiring stable network identities.
- **Use Case**: Databases or distributed systems like MongoDB or ZooKeeper.

### **YAML (`headless-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: headless-service    # Name of the Service
  namespace: kube-learn     # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  selector:                 # Selects Pods to manage
    app: stateful-app       # Matches Pods with label "app: stateful-app" (used by StatefulSet)
  ports:                    # Ports exposed by the Service
    - protocol: TCP         # Protocol used (TCP)
      port: 80              # Port exposed by the Service
      targetPort: 80        # Port on the Pod to forward traffic to
  clusterIP: None           # Makes the Service headless (no cluster IP, direct Pod DNS)
```

### **Usage**
- Provides DNS records for Pods in a StatefulSet (created later).
- Pods are accessible via `<pod-name>.<service-name>.<namespace>.svc.cluster.local`.

### **Testing**
- Testing requires a StatefulSet (see step 12). For now, apply the Service:
  ```bash
  kubectl apply -f headless-service.yaml  # Creates the Headless Service
  ```
- Verify the Service:
  ```bash
  kubectl get services -n kube-learn  # Lists Services, shows 'headless-service' with ClusterIP 'None'
  kubectl describe service headless-service -n kube-learn  # Shows Service details
  ```
- Full testing is covered in the StatefulSet section (step 12).

### **Dependencies**
- Namespace (`kube-learn`).
- StatefulSet with `app: stateful-app` label (for testing).

---

## **6️⃣ Service - LoadBalancer**

### **Explanation**
- **Purpose**: Exposes Pods externally via a cloud provider’s load balancer or local solution (e.g., MetalLB), assigning an external IP.
- **Use Case**: Public-facing web applications or APIs.

### **YAML (`loadbalancer-service.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Services
kind: Service               # Defines the resource type as a Service
metadata:                   # Metadata section for the Service
  name: nginx-loadbalancer  # Name of the Service
  namespace: kube-learn     # Namespace where the Service is created
spec:                       # Specification for the Service's desired state
  selector:                 # Selects Pods to route traffic to
    app: nginx              # Matches Pods with label "app: nginx"
  ports:                    # Ports exposed by the Service
    - protocol: TCP         # Protocol used (TCP)
      port: 80              # Port exposed by the Service
      targetPort: 80        # Port on the Pod to forward traffic to
  type: LoadBalancer        # Service type (exposes externally via load balancer)
```

### **Usage**
- Exposes the `nginx-deployment` Pods externally via an external IP.
- Requires a cloud provider or MetalLB in MicroK8s.

### **Testing**
1. Apply the Service:
   ```bash
   kubectl apply -f loadbalancer-service.yaml  # Creates the LoadBalancer Service
   ```
2. Verify the Service:
   ```bash
   kubectl get services -n kube-learn  # Lists Services, shows 'nginx-loadbalancer' with an external IP
   kubectl describe service nginx-loadbalancer -n kube-learn  # Shows Service details and endpoints
   ```
3. Test the Service:
   - Get the external IP:
     ```bash
     kubectl get svc nginx-loadbalancer -n kube-learn -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
     ```
   - Access `http://<external-ip>` in a browser or via `curl http://<external-ip>`.
   - In MicroK8s with MetalLB, ensure MetalLB is enabled:
     ```bash
     microk8s enable metallb:192.168.1.100-192.168.1.200  # Assigns IP range for LoadBalancer
     ```
   - If no external IP is assigned, check MetalLB logs or cloud provider configuration.

### **Dependencies**
- Namespace (`kube-learn`).
- Deployment (`nginx-deployment`) or Pod with `app: nginx` label.
- Cloud provider or MetalLB for LoadBalancer support.

---

## **7️⃣ ConfigMap**

### **Explanation**
- **Purpose**: Stores non-sensitive configuration data as key-value pairs, decoupling configuration from application code.
- **Use Case**: Setting environment variables or configuration files for applications.

### **YAML (`configmap.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for ConfigMaps
kind: ConfigMap             # Defines the resource type as a ConfigMap
metadata:                   # Metadata section for the ConfigMap
  name: app-config          # Name of the ConfigMap
  namespace: kube-learn     # Namespace where the ConfigMap is created
data:                       # Key-value pairs for configuration data
  APP_ENV: "production"     # Environment variable setting
  LOG_LEVEL: "debug"        # Log level setting
```

### **Usage**
- Mount ConfigMap as environment variables or files in Pods, Deployments, or StatefulSets.
- Below, we show usage in a Pod, Deployment, and StatefulSet.

### **Testing with Pod**
1. **YAML (`pod-with-configmap.yaml`)**
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: configmap-pod       # Name of the Pod
     namespace: kube-learn     # Namespace where the Pod is created
   spec:                       # Specification for the Pod's desired state
     containers:               # List of containers in the Pod
       - name: busybox         # Name of the container
         image: busybox        # Docker image (lightweight Linux utilities)
         command: ["sh", "-c", "env && sleep 3600"] # Prints environment variables and keeps running
         env:                  # Environment variables for the container
           - name: APP_ENV     # Name of the environment variable
             valueFrom:        # Source of the variable value
               configMapKeyRef:# References a ConfigMap key
                 name: app-config # Name of the ConfigMap
                 key: APP_ENV   # Key from the ConfigMap
           - name: LOG_LEVEL   # Name of the environment variable
             valueFrom:        # Source of the variable value
               configMapKeyRef:# References a ConfigMap key
                 name: app-config # Name of the ConfigMap
                 key: LOG_LEVEL # Key from the ConfigMap
   ```
2. Apply the ConfigMap and Pod:
   ```bash
   kubectl apply -f configmap.yaml  # Creates the ConfigMap
   kubectl apply -f pod-with-configmap.yaml  # Creates the Pod with ConfigMap
   ```
3. Verify and Test:
   ```bash
   kubectl get configmaps -n kube-learn  # Lists ConfigMaps, shows 'app-config'
   kubectl get pods -n kube-learn  # Confirms 'configmap-pod' is Running
   kubectl logs configmap-pod -n kube-learn  # Shows environment variables (APP_ENV=production, LOG_LEVEL=debug)
   ```

### **Testing with Deployment**
1. Update `deployment.yaml` to include ConfigMap:
   ```yaml
   apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
   kind: Deployment            # Defines the resource type as a Deployment
   metadata:                   # Metadata section for the Deployment
     name: nginx-deployment    # Name of the Deployment
     namespace: kube-learn     # Namespace where the Deployment is created
   spec:                       # Specification for the Deployment's desired state
     replicas: 3               # Number of Pod replicas to maintain
     selector:                 # Selector to match Pods managed by the Deployment
       matchLabels:            # Labels to match Pods
         app: nginx            # Label key-value pair to identify Pods
     template:                 # Template for creating Pods
       metadata:               # Metadata for Pods created by this Deployment
         labels:               # Labels assigned to Pods
           app: nginx          # Same label as in selector
       spec:                   # Specification for the Pods
         containers:           # List of containers in each Pod
           - name: nginx       # Name of the container
             image: nginx:latest # Docker image to use (Nginx web server, latest version)
             ports:             # Ports exposed by the container
               - containerPort: 80 # Port 80 (HTTP) for the container
             env:               # Environment variables for the container
               - name: APP_ENV  # Name of the environment variable
                 valueFrom:     # Source of the variable value
                   configMapKeyRef: # References a ConfigMap key
                     name: app-config # Name of the ConfigMap
                     key: APP_ENV # Key from the ConfigMap
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f deployment.yaml  # Updates the Deployment with ConfigMap
   kubectl get pods -n kube-learn -l app=nginx  # Lists Deployment Pods
   ```
   - Exec into a Pod to verify:
     ```bash
     kubectl exec -it <pod-name> -n kube-learn -- env  # Shows APP_ENV=production
     ```

### **Testing with StatefulSet**
- Covered in the StatefulSet section (step 12), where ConfigMap is mounted similarly.

### **Dependencies**
- Namespace (`kube-learn`).

---

## **8️⃣ Secret**

### **Explanation**
- **Purpose**: Stores sensitive data (e.g., passwords, API keys) in Base64-encoded format with access control for security.
- **Use Case**: Providing credentials for database connections.

### **YAML (`secret.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for Secrets
kind: Secret                # Defines the resource type as a Secret
metadata:                   # Metadata section for the Secret
  name: app-secret          # Name of the Secret
  namespace: kube-learn     # Namespace where the Secret is created
type: Opaque                # Type of Secret (generic key-value pairs)
data:                       # Base64-encoded sensitive data
  DB_PASSWORD: dGVzdHBhc3M= # Encoded value for "testpass"
```

### **Usage**
- Mount Secret as environment variables or files in Pods, Deployments, or StatefulSets.
- Below, we show usage in a Pod, Deployment, and StatefulSet.

### **Testing with Pod**
1. **YAML (`pod-with-secret.yaml`)**
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: secret-pod          # Name of the Pod
     namespace: kube-learn     # Namespace where the Pod is created
   spec:                       # Specification for the Pod's desired state
     containers:               # List of containers in the Pod
       - name: busybox         # Name of the container
         image: busybox        # Docker image (lightweight Linux utilities)
         command: ["sh", "-c", "env && sleep 3600"] # Prints environment variables and keeps running
         env:                  # Environment variables for the container
           - name: DB_PASSWORD # Name of the environment variable
             valueFrom:        # Source of the variable value
               secretKeyRef:   # References a Secret key
                 name: app-secret # Name of the Secret
                 key: DB_PASSWORD # Key from the Secret
   ```
2. Apply the Secret and Pod:
   ```bash
   kubectl apply -f secret.yaml  # Creates the Secret
   kubectl apply -f pod-with-secret.yaml  # Creates the Pod with Secret
   ```
3. Verify and Test:
   ```bash
   kubectl get secrets -n kube-learn  # Lists Secrets, shows 'app-secret'
   kubectl get pods -n kube-learn  # Confirms 'secret-pod' is Running
   kubectl logs secret-pod -n kube-learn  # Shows environment variable (DB_PASSWORD=testpass)
   ```

### **Testing with Deployment**
1. Update `deployment.yaml` to include Secret:
   ```yaml
   apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
   kind: Deployment            # Defines the resource type as a Deployment
   metadata:                   # Metadata section for the Deployment
     name: nginx-deployment    # Name of the Deployment
     namespace: kube-learn     # Namespace where the Deployment is created
   spec:                       # Specification for the Deployment's desired state
     replicas: 3               # Number of Pod replicas to maintain
     selector:                 # Selector to match Pods managed by the Deployment
       matchLabels:            # Labels to match Pods
         app: nginx            # Label key-value pair to identify Pods
     template:                 # Template for creating Pods
       metadata:               # Metadata for Pods created by this Deployment
         labels:               # Labels assigned to Pods
           app: nginx          # Same label as in selector
       spec:                   # Specification for the Pods
         containers:           # List of containers in each Pod
           - name: nginx       # Name of the container
             image: nginx:latest # Docker image to use (Nginx web server, latest version)
             ports:             # Ports exposed by the container
               - containerPort: 80 # Port 80 (HTTP) for the container
             env:               # Environment variables for the container
               - name: DB_PASSWORD # Name of the environment variable
                 valueFrom:     # Source of the variable value
                   secretKeyRef: # References a Secret key
                     name: app-secret # Name of the Secret
                     key: DB_PASSWORD # Key from the Secret
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f deployment.yaml  # Updates the Deployment with Secret
   kubectl get pods -n kube-learn -l app=nginx  # Lists Deployment Pods
   ```
   - Exec into a Pod to verify:
     ```bash
     kubectl exec -it <pod-name> -n kube-learn -- env  # Shows DB_PASSWORD=testpass
     ```

### **Testing with StatefulSet**
- Covered in the StatefulSet section (step 12).

### **Dependencies**
- Namespace (`kube-learn`).

---

## **9️⃣ Persistent Volume (PV)**

### **Explanation**
- **Purpose**: Represents a storage resource in the cluster, providing persistent storage for Pods.
- **Use Case**: Storing data that persists beyond Pod lifecycles (e.g., database files).

### **YAML (`pv.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for PersistentVolumes
kind: PersistentVolume      # Defines the resource type as a PersistentVolume
metadata:                   # Metadata section for the PV
  name: my-pv               # Name of the PersistentVolume
spec:                       # Specification for the PV's desired state
  capacity:                 # Storage capacity of the PV
    storage: 1Gi            # Allocates 1 gibibyte of storage
  accessModes:              # Access modes supported by the PV
    - ReadWriteOnce         # Allows read/write access by a single node
  hostPath:                 # Specifies the storage backend as hostPath
    path: "/mnt/data"       # Path on the host node where data is stored
```

### **Usage**
- Provides storage that a PVC can bind to, used by Pods, Deployments, or StatefulSets.
- Tested with a PVC and Pod below.

### **Testing**
1. Apply the PV:
   ```bash
   kubectl apply -f pv.yaml  # Creates the PersistentVolume
   ```
2. Verify the PV:
   ```bash
   kubectl get pv  # Lists PVs, shows 'my-pv' with status 'Available'
   kubectl describe pv my-pv  # Shows PV details
   ```
3. Testing requires a PVC (next section).

### **Dependencies**
- None (PV is cluster-wide).

---

## **10️⃣ PersistentVolumeClaim (PVC)**

### **Explanation**
- **Purpose**: Requests storage from a PV or dynamic provisioner, binding to a PV for use by Pods.
- **Use Case**: Enabling Pods to access persistent storage.

### **YAML (`pvc.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for PersistentVolumeClaims
kind: PersistentVolumeClaim # Defines the resource type as a PersistentVolumeClaim
metadata:                   # Metadata section for the PVC
  name: my-pvc              # Name of the PersistentVolumeClaim
  namespace: kube-learn     # Namespace where the PVC is created
spec:                       # Specification for the PVC's desired state
  accessModes:              # Requested access modes
    - ReadWriteOnce         # Requests read/write access by a single node
  resources:                # Resource requirements for the PVC
    requests:               # Specifies the minimum resources needed
      storage: 1Gi          # Requests 1 gibibyte of storage
```

### **Testing with Pod**
1. **YAML (`pod-with-pvc.yaml`)**
   ```yaml
   apiVersion: v1              # Specifies the Kubernetes API version for Pods
   kind: Pod                   # Defines the resource type as a Pod
   metadata:                   # Metadata section for the Pod
     name: pvc-pod             # Name of the Pod
     namespace: kube-learn     # Namespace where the Pod is created
   spec:                       # Specification for the Pod's desired state
     volumes:                  # List of volumes available to the Pod
       - name: storage         # Name of the volume
         persistentVolumeClaim:# Links to a PersistentVolumeClaim
           claimName: my-pvc   # Name of the PVC to use
     containers:               # List of containers in the Pod
       - name: busybox         # Name of the container
         image: busybox        # Docker image (lightweight Linux utilities)
         command: ["sh", "-c", "echo 'Test data' > /mnt/storage/data.txt && sleep 3600"] # Writes data and keeps running
         volumeMounts:          # Mounts the volume into the container
           - mountPath: "/mnt/storage" # Path inside the container where the volume is mounted
             name: storage       # Name of the volume to mount
   ```
2. Apply the PV, PVC, and Pod:
   ```bash
   kubectl apply -f pv.yaml  # Creates the PV
   kubectl apply -f pvc.yaml  # Creates the PVC
   kubectl apply -f pod-with-pvc.yaml  # Creates the Pod with PVC
   ```
3. Verify and Test:
   ```bash
   kubectl get pv  # Shows 'my-pv' as 'Bound' to 'my-pvc'
   kubectl get pvc -n kube-learn  # Shows 'my-pvc' as 'Bound'
   kubectl get pods -n kube-learn  # Confirms 'pvc-pod' is Running
   ```
   - Check data persistence:
     ```bash
     kubectl exec pvc-pod -n kube-learn -- cat /mnt/storage/data.txt  # Shows 'Test data'
     ```
     - Delete and recreate the Pod:
       ```bash
       kubectl delete pod pvc-pod -n kube-learn
       kubectl apply -f pod-with-pvc.yaml
       kubectl exec pvc-pod -n kube-learn -- cat /mnt/storage/data.txt  # Data persists
       ```

### **Testing with Deployment**
1. **YAML (`deployment-with-pvc.yaml`)**
   ```yaml
   apiVersion: apps/v1         # Specifies the Kubernetes API version for Deployments
   kind: Deployment            # Defines the resource type as a Deployment
   metadata:                   # Metadata section for the Deployment
     name: pvc-deployment      # Name of the Deployment
     namespace: kube-learn     # Namespace where the Deployment is created
   spec:                       # Specification for the Deployment's desired state
     replicas: 1               # Single replica to avoid multi-node issues with ReadWriteOnce
     selector:                 # Selector to match Pods managed by the Deployment
       matchLabels:            # Labels to match Pods
         app: pvc-app          # Label key-value pair to identify Pods
     template:                 # Template for creating Pods
       metadata:               # Metadata for Pods created by this Deployment
         labels:               # Labels assigned to Pods
           app: pvc-app        # Same label as in selector
       spec:                   # Specification for the Pods
         volumes:              # List of volumes available to the Pod
           - name: storage     # Name of the volume
             persistentVolumeClaim: # Links to a PersistentVolumeClaim
               claimName: my-pvc # Name of the PVC to use
         containers:           # List of containers in each Pod
           - name: busybox     # Name of the container
             image: busybox    # Docker image (lightweight Linux utilities)
             command: ["sh", "-c", "echo 'Test data' > /mnt/storage/data.txt && sleep 3600"] # Writes data
             volumeMounts:      # Mounts the volume into the container
               - mountPath: "/mnt/storage" # Path where the volume is mounted
                 name: storage   # Name of the volume to mount
   ```
2. Apply and Test:
   ```bash
   kubectl apply -f deployment-with-pvc.yaml  # Creates the Deployment with PVC
   kubectl get pods -n kube-learn -l app=pvc-app  # Lists Deployment Pods
   ```
   - Check data:
     ```bash
     kubectl exec <pod-name> -n kube-learn -- cat /mnt/storage/data.txt  # Shows 'Test data'
     ```
     - Delete Pod and verify persistence:
       ```bash
       kubectl delete pod <pod-name> -n kube-learn
       kubectl get pods -n kube-learn -l app=pvc-app  # New Pod is created
       kubectl exec <new-pod-name> -n kube-learn -- cat /mnt/storage/data.txt  # Data persists
       ```

### **Testing with StatefulSet**
- Covered in the StatefulSet section (step 12).

### **Dependencies**
- Namespace (`kube-learn`).
- PV (`my-pv`) for PVC binding.

---

## **11️⃣ Job**

### **Explanation**
- **Purpose**: Runs a task to completion, creating Pods that terminate once done.
- **Use Case**: Batch processing, data migrations, or one-off computations.

### **YAML (`job.yaml`)**
```yaml
apiVersion: batch/v1        # Specifies the Kubernetes API version for Jobs
kind: Job                   # Defines the resource type as a Job
metadata:                   # Metadata section for the Job
  name: simple-job          # Name of the Job
  namespace: kube-learn     # Namespace where the Job is created
spec:                       # Specification for the Job's desired state
  completions: 1            # Number of successful completions required
  parallelism: 1            # Number of Pods to run in parallel
  template:                 # Template for creating Pods
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
        - name: pi          # Name of the container
          image: perl       # Docker image (Perl for computing pi)
          command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"] # Computes pi to 2000 digits
      restartPolicy: Never # Ensures the Pod does not restart on completion
```

### **Usage**
- Runs a one-off task (computing pi) and terminates.
- Output is available in Pod logs.

### **Testing**
1. Apply the Job:
   ```bash
   kubectl apply -f job.yaml  # Creates the Job
   ```
2. Verify the Job:
   ```bash
   kubectl get jobs -n kube-learn  # Lists Jobs, shows 'simple-job'
   kubectl get pods -n kube-learn  # Shows Job Pod (e.g., 'simple-job-xxxxx') as Completed
   ```
3. Test the Job:
   ```bash
   kubectl logs <job-pod-name> -n kube-learn  # Shows pi value computed to 2000 digits
   ```

### **Dependencies**
- Namespace (`kube-learn`).

---

## **12️⃣ CronJob**

### **Explanation**
- **Purpose**: Schedules Jobs to run at specified times or intervals, like a cron scheduler.
- **Use Case**: Periodic tasks like backups or report generation.

### **YAML (`cronjob.yaml`)**
```yaml
apiVersion: batch/v1        # Specifies the Kubernetes API version for CronJobs
kind: CronJob               # Defines the resource type as a CronJob
metadata:                   # Metadata section for the CronJob
  name: simple-cronjob      # Name of the CronJob
  namespace: kube-learn     # Namespace where the CronJob is created
spec:                       # Specification for the CronJob's desired state
  schedule: "*/5 * * * *"   # Runs every 5 minutes (cron schedule)
  jobTemplate:              # Template for Jobs created by the CronJob
    spec:                   # Specification for the Jobs
      template:             # Template for creating Pods
        spec:               # Specification for the Pods
          containers:       # List of containers in each Pod
            - name: hello   # Name of the container
              image: busybox # Docker image (lightweight Linux utilities)
              command: ["echo", "Hello from CronJob"] # Prints a message
          restartPolicy: OnFailure # Restarts the Pod on failure
```

### **Usage**
- Schedules a Job to print a message every 5 minutes.
- Job Pods are created and terminated per schedule.

### **Testing**
1. Apply the CronJob:
   ```bash
   kubectl apply -f cronjob.yaml  # Creates the CronJob
   ```
2. Verify the CronJob:
   ```bash
   kubectl get cronjobs -n kube-learn  # Lists CronJobs, shows 'simple-cronjob'
   ```
3. Test the CronJob:
   - Wait for the next 5-minute interval or trigger manually:
     ```bash
     kubectl create job --from=cronjob/simple-cronjob manual-job -n kube-learn  # Creates a manual Job
     ```
   - Check Job Pods:
     ```bash
     kubectl get pods -n kube-learn  # Shows CronJob Pods (e.g., 'manual-job-xxxxx')
     kubectl logs <job-pod-name> -n kube-learn  # Shows 'Hello from CronJob'
     ```

### **Dependencies**
- Namespace (`kube-learn`).

---

## **13️⃣ StatefulSet**

### **Explanation**
- **Purpose**: Manages stateful applications with stable Pod identities, persistent storage, and ordered operations.
- **Use Case**: Databases (e.g., MySQL, Cassandra) or systems requiring unique identities.

### **YAML (`statefulset.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for StatefulSets
kind: StatefulSet           # Defines the resource type as a StatefulSet
metadata:                   # Metadata section for the StatefulSet
  name: web-stateful        # Name of the StatefulSet
  namespace: kube-learn     # Namespace where the StatefulSet is created
spec:                       # Specification for the StatefulSet's desired state
  serviceName: headless-service # Name of the headless Service for DNS resolution
  replicas: 2               # Number of Pod replicas to maintain
  selector:                 # Selector to match Pods managed by the StatefulSet
    matchLabels:            # Labels to match Pods
      app: stateful-app     # Label key-value pair to identify Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this StatefulSet
      labels:               # Labels assigned to Pods
        app: stateful-app   # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
        - name: nginx       # Name of the container
          image: nginx:latest # Docker image to use (Nginx web server, latest version)
          ports:             # Ports exposed by the container
            - containerPort: 80 # Port 80 (HTTP) for the container
          volumeMounts:      # Mounts volumes into the container
            - name: data     # Name of the volume to mount
              mountPath: "/usr/share/nginx/html" # Path for persistent data
          env:               # Environment variables for the container
            - name: APP_ENV  # Name of the environment variable
              valueFrom:     # Source of the variable value
                configMapKeyRef: # References a ConfigMap key
                  name: app-config # Name of the ConfigMap
                  key: APP_ENV # Key from the ConfigMap
            - name: DB_PASSWORD # Name of the environment variable
              valueFrom:     # Source of the variable value
                secretKeyRef: # References a Secret key
                  name: app-secret # Name of the Secret
                  key: DB_PASSWORD # Key from the Secret
  volumeClaimTemplates:     # Template for creating PVCs for each Pod
    - metadata:             # Metadata for the PVC
        name: data          # Name of the PVC (used in volumeMounts)
      spec:                 # Specification for the PVC
        accessModes: ["ReadWriteOnce"] # Requests read/write access by a single node
        resources:          # Resource requirements for the PVC
          requests:         # Specifies the minimum resources needed
            storage: 1Gi    # Requests 1 gibibyte of storage
```

### **Usage**
- Manages 2 Nginx Pods with stable identities (e.g., `web-stateful-0`, `web-stateful-1`).
- Each Pod gets its own PVC for persistent storage.
- Uses ConfigMap and Secret for configuration and credentials.

### **Testing**
1. Apply the Headless Service and StatefulSet:
   ```bash
   kubectl apply -f headless-service.yaml  # Creates the Headless Service
   kubectl apply -f configmap.yaml  # Ensures ConfigMap is available
   kubectl apply -f secret.yaml  # Ensures Secret is available
   kubectl apply -f statefulset.yaml  # Creates the StatefulSet
   ```
2. Verify the StatefulSet:
   ```bash
   kubectl get statefulsets -n kube-learn  # Lists StatefulSets, shows 'web-stateful'
   kubectl get pods -n kube-learn -l app=stateful-app  # Shows Pods (web-stateful-0, web-stateful-1)
   kubectl get pvc -n kube-learn  # Shows PVCs (data-web-stateful-0, data-web-stateful-1)
   ```
3. Test the StatefulSet:
   - Write data to a Pod:
     ```bash
     kubectl exec web-stateful-0 -n kube-learn -- sh -c "echo 'Stateful data' > /usr/share/nginx/html/test.txt"
     ```
   - Verify persistence:
     ```bash
     kubectl delete pod web-stateful-0 -n kube-learn  # Deletes Pod, StatefulSet recreates it
     kubectl exec web-stateful-0 -n kube-learn -- cat /usr/share/nginx/html/test.txt  # Shows 'Stateful data'
     ```
   - Test DNS via Headless Service:
     ```bash
     kubectl run -i --tty test-pod --image=busybox --rm --restart=Never -n kube-learn -- sh
     ```
     - Inside the Pod, run:
       ```bash
       nslookup web-stateful-0.headless-service.kube-learn.svc.cluster.local  # Resolves to Pod IP
       wget -qO- http://web-stateful-0.headless-service.kube-learn.svc.cluster.local:80  # Accesses Pod
       ```
   - Verify ConfigMap and Secret:
     ```bash
     kubectl exec web-stateful-0 -n kube-learn -- env  # Shows APP_ENV=production, DB_PASSWORD=testpass
     ```

### **Dependencies**
- Namespace (`kube-learn`).
- Headless Service (`headless-service`).
- ConfigMap (`app-config`).
- Secret (`app-secret`).

---

## **14️⃣ Ingress**

### **Explanation**
- **Purpose**: Routes external HTTP/HTTPS traffic to Services based on URL paths or hostnames using an Ingress controller.
- **Use Case**: Exposing web applications with custom domains or paths.

### **YAML (`ingress.yaml`)**
```yaml
apiVersion: networking.k8s.io/v1 # Specifies the Kubernetes API version for Ingress
kind: Ingress                    # Defines the resource type as an Ingress
metadata:                        # Metadata section for the Ingress
  name: nginx-ingress            # Name of the Ingress
  namespace: kube-learn         # Namespace where the Ingress is created
spec:                            # Specification for the Ingress's desired state
  rules:                         # Routing rules for the Ingress
    - host: app.local            # Domain name for this rule
      http:                      # HTTP-specific configuration
        paths:                   # Paths to route traffic
          - path: /              # Root path
            pathType: Prefix     # Matches any path starting with "/"
            backend:             # Destination for traffic
              service:           # Links to a Service
                name: nginx-clusterip # Name of the Service to route to
                port:            # Port on the Service
                  number: 80     # Port 80 (HTTP)
```

### **Usage**
- Routes `http://app.local/` to the `nginx-clusterip` Service.
- Requires an Ingress controller (e.g., Nginx Ingress).

### **Testing**
1. Apply the Ingress:
   ```bash
   kubectl apply -f ingress.yaml  # Creates the Ingress
   ```
2. Verify the Ingress:
   ```bash
   kubectl get ingress -n kube-learn  # Lists Ingresses, shows 'nginx-ingress'
   kubectl describe ingress nginx-ingress -n kube-learn  # Shows Ingress details and rules
   ```
3. Test the Ingress:
   - In MicroK8s, enable the Ingress add-on:
     ```bash
     microk8s enable ingress  # Installs Nginx Ingress controller
     ```
   - Get the Ingress IP:
     ```bash
     kubectl get ingress -n kube-learn -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'
     ```
   - Update `/etc/hosts` to map `app.local` to the Ingress IP:
     ```bash
     echo "<ingress-ip> app.local" | sudo tee -a /etc/hosts
     ```
   - Access `http://app.local` in a browser or via `curl http://app.local` to see the Nginx page.

### **Dependencies**
- Namespace (`kube-learn`).
- Service (`nginx-clusterip`).
- Deployment or Pod with `app: nginx` label.
- Ingress controller.

---

## **15️⃣ RBAC - Role and RoleBinding**

### **Explanation**
- **Purpose**: Controls access to Kubernetes resources based on user or service account roles, enforcing security.
- **Use Case**: Restricting developers to specific namespaces or actions (e.g., read-only access).

### **YAML (`rbac.yaml`)**
```yaml
apiVersion: rbac.authorization.k8s.io/v1 # Specifies the Kubernetes API version for RBAC
kind: Role                        # Defines the resource type as a Role
metadata:                         # Metadata section for the Role
  name: pod-reader                # Name of the Role
  namespace: kube-learn          # Namespace where the Role applies
rules:                            # Rules defining permissions
  - apiGroups: [""]               # Core API group (for Pods)
    resources: ["pods"]           # Resource type (Pods)
    verbs: ["get", "list", "watch"] # Allowed actions on Pods

---
apiVersion: rbac.authorization.k8s.io/v1 # Specifies the Kubernetes API version for RBAC
kind: RoleBinding                 # Defines the resource type as a RoleBinding
metadata:                         # Metadata section for the RoleBinding
  name: pod-reader-binding        # Name of the RoleBinding
  namespace: kube-learn          # Namespace where the RoleBinding applies
subjects:                         # Subjects (users or service accounts) granted the Role
  - kind: User                    # Type of subject (User)
    name: student                 # Name of the user
    apiGroup: rbac.authorization.k8s.io # API group for RBAC subjects
roleRef:                          # Reference to the Role being bound
  kind: Role                      # Type of resource being referenced
  name: pod-reader                # Name of the Role
  apiGroup: rbac.authorization.k8s.io # API group for RBAC roles
```

### **Usage**
- Grants user `student` read-only access to Pods in the `kube-learn` namespace.
- Applied to control access for specific users or service accounts.

### **Testing**
1. Apply the RBAC resources:
   ```bash
   kubectl apply -f rbac.yaml  # Creates the Role and RoleBinding
   ```
2. Verify the RBAC:
   ```bash
   kubectl get role,rolebinding -n kube-learn  # Lists Roles and RoleBindings
   kubectl describe role pod-reader -n kube-learn  # Shows Role details
   kubectl describe rolebinding pod-reader-binding -n kube-learn  # Shows RoleBinding details
   ```
3. Test the RBAC:
   - Configure `kubectl` to use the `student` user (requires cluster admin to set up user credentials, e.g., via certificate or token).
   - As `student`, run:
     ```bash
     kubectl get pods -n kube-learn  # Should succeed
     kubectl delete pod nginx-pod -n kube-learn  # Should fail (no 'delete' permission)
     ```
   - If user setup is complex, simulate with a service account:
     ```yaml
     apiVersion: v1
     kind: ServiceAccount
     metadata:
       name: test-sa
       namespace: kube-learn
     ```
     ```yaml
     apiVersion: rbac.authorization.k8s.io/v1
     kind: RoleBinding
     metadata:
       name: pod-reader-sa-binding
       namespace: kube-learn
     subjects:
       - kind: ServiceAccount
         name: test-sa
         namespace: kube-learn
     roleRef:
       kind: Role
       name: pod-reader
       apiGroup: rbac.authorization.k8s.io
     ```
     - Apply and test:
       ```bash
       kubectl apply -f sa.yaml
       kubectl apply -f sa-rolebinding.yaml
       kubectl auth can-i get pods --as=system:serviceaccount:kube-learn:test-sa -n kube-learn  # Should return 'yes'
       kubectl auth can-i delete pods --as=system:serviceaccount:kube-learn:test-sa -n kube-learn  # Should return 'no'
       ```

### **Dependencies**
- Namespace (`kube-learn`).
- User or service account (`student` or `test-sa`).

---

## **16️⃣ DaemonSet**

### **Explanation**
- **Purpose**: Ensures a Pod runs on every node (or a subset) in the cluster, typically for cluster-wide services.
- **Use Case**: Running monitoring agents (e.g., Prometheus) or log collectors on all nodes.

### **YAML (`daemonset.yaml`)**
```yaml
apiVersion: apps/v1         # Specifies the Kubernetes API version for DaemonSets
kind: DaemonSet             # Defines the resource type as a DaemonSet
metadata:                   # Metadata section for the DaemonSet
  name: monitoring-agent    # Name of the DaemonSet
  namespace: kube-learn     # Namespace where the DaemonSet is created
spec:                       # Specification for the DaemonSet's desired state
  selector:                 # Selector to match Pods managed by the DaemonSet
    matchLabels:            # Labels to match Pods
      app: monitoring       # Label key-value pair to identify Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this DaemonSet
      labels:               # Labels assigned to Pods
        app: monitoring     # Same label as in selector
    spec:                   # Specification for the Pods
      containers:           # List of containers in each Pod
        - name: fluentd     # Name of the container
          image: fluent/fluentd # Docker image (Fluentd for log collection)
          resources:          # Resource limits for the container
            limits:           # Maximum resources
              memory: "200Mi" # Memory limit
            requests:         # Minimum resources
              memory: "100Mi" # Memory request
```

### **Usage**
- Runs a Fluentd Pod on every node for log collection.
- Automatically scales with cluster nodes.

### **Testing**
1. Apply the DaemonSet:
   ```bash
   kubectl apply -f daemonset.yaml  # Creates the DaemonSet
   ```
2. Verify the DaemonSet:
   ```bash
   kubectl get daemonsets -n kube-learn  # Lists DaemonSets, shows 'monitoring-agent'
   kubectl get pods -n kube-learn -l app=monitoring  # Lists Pods, one per node
   kubectl describe daemonset monitoring-agent -n kube-learn  # Shows DaemonSet details
   ```
3. Test the DaemonSet:
   - Check Pods are running on all nodes:
     ```bash
     kubectl get pods -n kube-learn -l app=monitoring -o wide  # Shows Pods with node assignments
     ```
   - Verify Fluentd is running:
     ```bash
     kubectl logs <pod-name> -n kube-learn  # Shows Fluentd logs
     ```

### **Dependencies**
- Namespace (`kube-learn`).

---

## **17️⃣ NetworkPolicy**

### **Explanation**
- **Purpose**: Defines rules for network traffic to and from Pods, enhancing security by restricting communication.
- **Use Case**: Allowing only specific Pods to communicate with a database or service.

### **YAML (`networkpolicy.yaml`)**
```yaml
apiVersion: networking.k8s.io/v1 # Specifies the Kubernetes API version for NetworkPolicies
kind: NetworkPolicy              # Defines the resource type as a NetworkPolicy
metadata:                        # Metadata section for the NetworkPolicy
  name: allow-nginx-access       # Name of the NetworkPolicy
  namespace: kube-learn         # Namespace where the NetworkPolicy applies
spec:                            # Specification for the NetworkPolicy's desired state
  podSelector:                   # Selects Pods to which this policy applies
    matchLabels:                 # Labels to match Pods
      app: nginx                 # Applies to Pods with label "app: nginx"
  policyTypes:                   # Types of traffic controlled
    - Ingress                    # Controls incoming traffic
  ingress:                       # Rules for incoming traffic
    - from:                      # Sources allowed to send traffic
        - podSelector:           # Selects source Pods
            matchLabels:         # Labels to match source Pods
              app: pvc-app       # Allows traffic from Pods with label "app: pvc-app"
      ports:                     # Ports allowed for incoming traffic
        - protocol: TCP          # Protocol (TCP)
          port: 80               # Port 80 (HTTP)
```

### **Usage**
- Restricts traffic to `app: nginx` Pods (e.g., from `nginx-deployment`) to only allow connections from `app: pvc-app` Pods (e.g., `pvc-pod`).
- Enhances security by limiting network access.

### **Testing**
1. Apply the NetworkPolicy (assuming `nginx-deployment` and `pvc-pod` are running):
   ```bash
   kubectl apply -f networkpolicy.yaml  # Creates the NetworkPolicy
   ```
2. Verify the NetworkPolicy:
   ```bash
   kubectl get networkpolicies -n kube-learn  # Lists NetworkPolicies, shows 'allow-nginx-access'
   kubectl describe networkpolicy allow-nginx-access -n kube-learn  # Shows policy details
   ```
3. Test the NetworkPolicy:
   - From `pvc-pod` (allowed):
     ```bash
     kubectl exec pvc-pod -n kube-learn -- wget -qO- http://nginx-clusterip:80  # Should succeed
     ```
   - Create a test Pod without `app: pvc-app` label:
     ```yaml
     apiVersion: v1
     kind: Pod
     metadata:
       name: test-pod
       namespace: kube-learn
     spec:
       containers:
       - name: busybox
         image: busybox
         command: ["sleep", "3600"]
     ```
     ```bash
     kubectl apply -f test-pod.yaml
     kubectl exec test-pod -n kube-learn -- wget -qO- http://nginx-clusterip:80  # Should fail (timeout)
     ```
   - Clean up test Pod:
     ```bash
     kubectl delete pod test-pod -n kube-learn
     ```

### **Dependencies**
- Namespace (`kube-learn`).
- Deployment (`nginx-deployment`) with `app: nginx` label.
- Pod (`pvc-pod`) with `app: pvc-app` label.
- Network plugin supporting NetworkPolicy (e.g., Calico).

---

## **End-to-End Flow**

This section summarizes the deployment and testing order for all components, ensuring students can follow a logical progression. Each step builds on previous ones, respecting dependencies (e.g., Namespace first, Headless Service before StatefulSet).

### **Step-by-Step Deployment and Testing**
1. **Namespace**: Create the `kube-learn` namespace to isolate resources.
   ```bash
   kubectl apply -f namespace.yaml
   kubectl get namespaces
   ```
2. **RBAC**: Set up Role and RoleBinding to control access (test with service account if user setup is complex).
   ```bash
   kubectl apply -f rbac.yaml
   kubectl get role,rolebinding -n kube-learn
   kubectl auth can-i get pods --as=system:serviceaccount:kube-learn:test-sa -n kube-learn
   ```
3. **ConfigMap**: Create and test with a Pod and Deployment.
   ```bash
   kubectl apply -f configmap.yaml
   kubectl apply -f pod-with-configmap.yaml
   kubectl logs configmap-pod -n kube-learn
   kubectl apply -f deployment.yaml  # With ConfigMap env
   kubectl exec <deployment-pod> -n kube-learn -- env
   ```
4. **Secret**: Create and test with a Pod and Deployment.
   ```bash
   kubectl apply -f secret.yaml
   kubectl apply -f pod-with-secret.yaml
   kubectl logs secret-pod -n kube-learn
   kubectl apply -f deployment.yaml  # With Secret env
   kubectl exec <deployment-pod> -n kube-learn -- env
   ```
5. **Persistent Volume (PV)**: Create the PV for storage.
   ```bash
   kubectl apply -f pv.yaml
   kubectl get pv
   ```
6. **PersistentVolumeClaim (PVC)**: Create and test with a Pod and Deployment.
   ```bash
   kubectl apply -f pvc.yaml
   kubectl apply -f pod-with-pvc.yaml
   kubectl exec pvc-pod -n kube-learn -- cat /mnt/storage/data.txt
   kubectl apply -f deployment-with-pvc.yaml
   kubectl exec <pvc-deployment-pod> -n kube-learn -- cat /mnt/storage/data.txt
   ```
7. **Pod**: Create and test the standalone Nginx Pod.
   ```bash
   kubectl apply -f pod.yaml
   kubectl port-forward pod/nginx-pod 8080:80 -n kube-learn
   curl http://localhost:8080
   ```
8. **Deployment**: Create and test the Deployment, reusing the Service.
   ```bash
   kubectl apply -f deployment.yaml  # Ensure ConfigMap/Secret are included
   kubectl get pods -n kube-learn -l app=nginx
   ```
9. **Service - ClusterIP**: Create and test with the Pod and Deployment.
   ```bash
   kubectl apply -f clusterip-service.yaml
   kubectl port-forward svc/nginx-clusterip 8080:80 -n kube-learn
   curl http://localhost:8080
   ```
10. **Service - LoadBalancer**: Create and test external access.
    ```bash
    kubectl apply -f loadbalancer-service.yaml
    kubectl get svc nginx-loadbalancer -n kube-learn
    curl http://<external-ip>
    ```
11. **Service - Headless**: Create for StatefulSet.
    ```bash
    kubectl apply -f headless-service.yaml
    kubectl get services -n kube-learn
    ```
12. **StatefulSet**: Create and test with Headless Service, ConfigMap, Secret, and PVCs.
    ```bash
    kubectl apply -f statefulset.yaml
    kubectl get pods -n kube-learn -l app=stateful-app
    kubectl exec web-stateful-0 -n kube-learn -- cat /usr/share/nginx/html/test.txt
    kubectl exec web-stateful-0 -n kube-learn -- env
    ```
13. **Job**: Create and test the one-off task.
    ```bash
    kubectl apply -f job.yaml
    kubectl logs <job-pod-name> -n kube-learn
    ```
14. **CronJob**: Create and test the scheduled task.
    ```bash
    kubectl apply -f cronjob.yaml
    kubectl create job --from=cronjob/simple-cronjob manual-job -n kube-learn
    kubectl logs <job-pod-name> -n kube-learn
    ```
15. **DaemonSet**: Create and test the node-level Pods.
    ```bash
    kubectl apply -f daemonset.yaml
    kubectl get pods -n kube-learn -l app=monitoring -o wide
    ```
16. **NetworkPolicy**: Create and test traffic restrictions.
    ```bash
    kubectl apply -f networkpolicy.yaml
    kubectl exec pvc-pod -n kube-learn -- wget -qO- http://nginx-clusterip:80
    kubectl apply -f test-pod.yaml
    kubectl exec test-pod -n kube-learn -- wget -qO- http://nginx-clusterip:80  # Should fail
    ```
17. **Ingress**: Create and test external routing.
    ```bash
    kubectl apply -f ingress.yaml
    kubectl get ingress -n kube-learn
    curl http://app.local
    ```

### **Cleanup**
Delete the namespace to remove all resources:
```bash
kubectl delete namespace kube-learn  # Deletes all resources in the namespace
```

---

## **Summary**
This cheat sheet is tailored for students, providing:
- **Individual Explanations**: Clear purpose and use case for each component.
- **Commented Configurations**: Simple YAML files with inline comments.
- **Usage Examples**: Demonstrates how to use each component (e.g., ConfigMap/Secret in Pods, Deployments, StatefulSets).
- **Testing Steps**: Specific commands to verify each component, often with related resources (e.g., PVC with Pod, Deployment, StatefulSet).
- **End-to-End Flow**: A logical progression for deploying and testing all components, with cleanup.
- **MicroK8s Compatibility**: Uses `hostPath` for PVs, suitable for your MicroK8s setup.

The modular structure allows students to learn one concept at a time, test it thoroughly, and build understanding progressively. 🚀S