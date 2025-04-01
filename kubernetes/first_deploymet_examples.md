# Complete Kubernetes Deployment Guide with Namespace

This document contains all necessary YAML configurations for deploying a Kubernetes application with Pods, Deployments, Services, ConfigMaps, Secrets, Persistent Volumes, and Ingress within a specific Namespace.

---

## **1️⃣ Namespace (`namespace.yaml`)**
```yaml
apiVersion: v1              # Specifies the Kubernetes API version for this resource
kind: Namespace             # Defines the type of resource (Namespace in this case)
metadata:                   # Metadata section contains information about the resource
  name: my-namespace        # Name of the namespace; all resources will be created under this scope
```

---

## **2️⃣ Pod Definition (`pod.yaml`)**
```yaml
apiVersion: v1              # API version for Pods
kind: Pod                   # Resource type is a Pod
metadata:                   # Metadata for identifying the Pod
  name: my-pod              # Name of the Pod
  namespace: my-namespace   # Specifies the namespace this Pod belongs to
spec:                       # Specification of the Pod's desired state
  containers:               # List of containers to run in the Pod
    - name: nginx-container # Name of the container (for reference)
      image: nginx           # Docker image to use (nginx web server)
      ports:                 # Ports the container exposes
        - containerPort: 80  # Port 80 (HTTP) inside the container
```

---

## **3️⃣ Deployment (`deployment.yaml`)**
```yaml
apiVersion: apps/v1         # API version for Deployments (from apps group)
kind: Deployment            # Resource type is a Deployment
metadata:                   # Metadata for the Deployment
  name: my-deployment       # Name of the Deployment
  namespace: my-namespace   # Namespace scope
spec:                       # Specification of the Deployment
  replicas: 3               # Number of Pod replicas to maintain
  selector:                 # How the Deployment identifies its Pods
    matchLabels:            # Matches Pods with these labels
      app: my-app           # Label key-value pair to select Pods
  template:                 # Template for creating Pods
    metadata:               # Metadata for Pods created by this Deployment
      labels:               # Labels assigned to Pods
        app: my-app         # Same label as in selector
    spec:                   # Pod specification
      containers:           # Containers in each Pod
        - name: nginx-container # Container name
          image: nginx         # Image to use
          ports:               # Ports exposed by the container
            - containerPort: 80 # Port 80 for HTTP
```

---

## **4️⃣ Service (`service.yaml`)**
```yaml
apiVersion: v1              # API version for Services
kind: Service               # Resource type is a Service
metadata:                   # Metadata for the Service
  name: my-service          # Name of the Service
  namespace: my-namespace   # Namespace scope
spec:                       # Specification of the Service
  selector:                 # Selects Pods to expose
    app: my-app             # Matches Pods with label "app: my-app"
  ports:                    # Ports the Service exposes
    - protocol: TCP         # Protocol (TCP or UDP)
      port: 80              # Port exposed by the Service
      targetPort: 80        # Port on the Pod to forward traffic to
  type: ClusterIP           # Service type (default, internal to cluster)
```

---

## **5️⃣ ConfigMap (`configmap.yaml`)**
```yaml
apiVersion: v1              # API version for ConfigMaps
kind: ConfigMap             # Resource type is a ConfigMap
metadata:                   # Metadata for the ConfigMap
  name: my-config           # Name of the ConfigMap
  namespace: my-namespace   # Namespace scope
data:                       # Data section for key-value pairs
  APP_ENV: "production"     # Environment variable for the app
  LOG_LEVEL: "info"         # Log level setting
```

---

## **6️⃣ Secret (`secret.yaml`)**
```yaml
apiVersion: v1              # API version for Secrets
kind: Secret                # Resource type is a Secret
metadata:                   # Metadata for the Secret
  name: my-secret           # Name of the Secret
  namespace: my-namespace   # Namespace scope
type: Opaque                # Type of Secret (generic key-value pairs)
data:                       # Data section (Base64 encoded)
  DB_PASSWORD: bXlTdXBlclBhc3M=  # Encoded "mySuperPass"
```

---

## **7️⃣ Persistent Volume & PVC (`pv-pvc.yaml`)**
```yaml
apiVersion: v1              # API version for PV
kind: PersistentVolume      # Resource type is a PersistentVolume
metadata:                   # Metadata for the PV
  name: my-pv               # Name of the PV
spec:                       # Specification of the PV
  capacity:                 # Storage capacity
    storage: 1Gi            # 1 Gibibyte of storage
  accessModes:              # Access modes for the volume
    - ReadWriteOnce         # Can be mounted as read-write by one node
  hostPath:                 # Type of storage (local host path for simplicity)
    path: "/mnt/data"       # Path on the host where data is stored

---
apiVersion: v1              # API version for PVC
kind: PersistentVolumeClaim # Resource type is a PVC
metadata:                   # Metadata for the PVC
  name: my-pvc              # Name of the PVC
  namespace: my-namespace   # Namespace scope
spec:                       # Specification of the PVC
  accessModes:              # Requested access modes
    - ReadWriteOnce         # Matches PV's access mode
  resources:                # Requested resources
    requests:               # Minimum requirements
      storage: 1Gi          # Requests 1Gi of storage
```

---

## **8️⃣ Pod with PVC (`pod-with-pvc.yaml`)**
```yaml
apiVersion: v1              # API version for Pods
kind: Pod                   # Resource type is a Pod
metadata:                   # Metadata for the Pod
  name: pod-with-pvc        # Name of the Pod
  namespace: my-namespace   # Namespace scope
spec:                       # Specification of the Pod
  volumes:                  # Volumes available to the Pod
    - name: my-storage      # Name of the volume
      persistentVolumeClaim:# Links to a PVC
        claimName: my-pvc    # Name of the PVC to use
  containers:               # Containers in the Pod
    - name: busybox         # Container name
      image: busybox        # Image (lightweight Linux utils)
      command: [ "sleep", "3600" ] # Keeps the container running for 1 hour
      volumeMounts:          # Mounts the volume into the container
        - mountPath: "/mnt/storage" # Path inside the container
          name: my-storage     # Name of the volume to mount
```

---

## **9️⃣ Ingress Configuration (`ingress.yaml`)**
```yaml
apiVersion: networking.k8s.io/v1 # API version for Ingress
kind: Ingress                    # Resource type is an Ingress
metadata:                        # Metadata for the Ingress
  name: my-ingress               # Name of the Ingress
  namespace: my-namespace        # Namespace scope
spec:                            # Specification of the Ingress
  rules:                         # Routing rules
    - host: myapp.local          # Domain name for this rule
      http:                      # HTTP-specific configuration
        paths:                   # Paths to route
          - path: /              # Root path
            pathType: Prefix     # Matches any path starting with "/"
            backend:             # Destination for traffic
              service:           # Links to a Service
                name: my-service # Name of the Service
                port:            # Port on the Service
                  number: 80     # Port 80 (HTTP)
```

---

## **🔹 Applying All YAML Files**

```bash
kubectl apply -f namespace.yaml
kubectl apply -f pod.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f pv-pvc.yaml
kubectl apply -f pod-with-pvc.yaml
kubectl apply -f ingress.yaml
```

---

## **🔹 Verifying Deployment in Namespace**

```bash
kubectl get all -n my-namespace
kubectl get pods -n my-namespace
kubectl get deployments -n my-namespace
kubectl get services -n my-namespace
kubectl get pv
kubectl get pvc -n my-namespace
kubectl get ingress -n my-namespace
```

---

## **🔹 Cleanup**

```bash
kubectl delete namespace my-namespace
```

This document includes **all required Kubernetes configurations** with a dedicated namespace. 🚀🔥
