# 📦 Kubernetes Storage Cheat Sheet

This cheat sheet covers common Kubernetes storage options, including `emptyDir`, `PersistentVolume` (PV) with `PersistentVolumeClaim` (PVC), dynamic provisioning with PVC, generic ephemeral volumes, and StatefulSet with `volumeClaimTemplates`. Each YAML example includes inline comments explaining the purpose of every line.

---

## 1. 🔹 emptyDir
- Ephemeral storage tied to Pod lifecycle
- Data is deleted when the Pod is removed
- Great for caching, temp files

```yaml
apiVersion: v1                        # Specifies the Kubernetes API version for Pods
kind: Pod                             # Defines the resource type as a Pod
metadata:                             # Metadata section for the Pod
  name: emptydir-pod                  # Name of the Pod
spec:                                 # Specification for the Pod's desired state
  containers:                         # List of containers in the Pod
    - name: app                       # Name of the container
      image: nginx                    # Container image to use (Nginx web server)
      volumeMounts:                   # Mount points for volumes inside the container
        - mountPath: /tmp/cache       # Path in the container where the volume is mounted
          name: temp-storage          # Name of the volume to mount (matches volume definition)
  volumes:                            # List of volumes available to the Pod
    - name: temp-storage              # Name of the volume
      emptyDir: {}                    # Defines an emptyDir volume, ephemeral and tied to Pod lifecycle
```

---

## 2. 🔹 PersistentVolume (PV) + PersistentVolumeClaim (PVC)
- Manually create the PV and the PVC
- Useful for fine-grained control
- Good for hostPath, NFS, or fixed resources

```yaml
# PV
apiVersion: v1                        # Specifies the Kubernetes API version for PersistentVolumes
kind: PersistentVolume                # Defines the resource type as a PersistentVolume
metadata:                             # Metadata section for the PV
  name: my-pv                         # Name of the PersistentVolume
spec:                                 # Specification for the PV's desired state
  capacity:                           # Defines the storage capacity of the PV
    storage: 1Gi                      # Allocates 1 gibibyte of storage
  accessModes:                        # List of access modes supported by the PV
    - ReadWriteOnce                   # Allows read/write access by a single node
  hostPath:                           # Specifies the storage backend as hostPath
    path: "/mnt/data"                 # Path on the host node where data is stored

---
# PVC
apiVersion: v1                        # Specifies the Kubernetes API version for PersistentVolumeClaims
kind: PersistentVolumeClaim           # Defines the resource type as a PersistentVolumeClaim
metadata:                             # Metadata section for the PVC
  name: my-pvc                        # Name of the PersistentVolumeClaim
spec:                                 # Specification for the PVC's desired state
  accessModes:                        # List of access modes requested by the PVC
    - ReadWriteOnce                   # Requests read/write access by a single node
  resources:                          # Resource requirements for the PVC
    requests:                         # Specifies the minimum resources needed
      storage: 1Gi                    # Requests 1 gibibyte of storage
```

---

## 3. 🔹 PVC Only (Dynamic Provisioning with StorageClass)
- PVC triggers PV creation dynamically
- No need to create PV manually
- Uses the default StorageClass (like `microk8s-hostpath`)

```yaml
apiVersion: v1                        # Specifies the Kubernetes API version for PersistentVolumeClaims
kind: PersistentVolumeClaim           # Defines the resource type as a PersistentVolumeClaim
metadata:                             # Metadata section for the PVC
  name: dynamic-pvc                   # Name of the PersistentVolumeClaim
spec:                                 # Specification for the PVC's desired state
  accessModes:                        # List of access modes requested by the PVC
    - ReadWriteOnce                   # Requests read/write access by a single node
  resources:                          # Resource requirements for the PVC
    requests:                         # Specifies the minimum resources needed
      storage: 1Gi                    # Requests 1 gibibyte of storage
  storageClassName: microk8s-hostpath # Specifies the StorageClass for dynamic provisioning
```

```yaml
apiVersion: v1                        # Specifies the Kubernetes API version for Pods
kind: Pod                             # Defines the resource type as a Pod
metadata:                             # Metadata section for the Pod
  name: dynamic-pod                   # Name of the Pod
spec:                                 # Specification for the Pod's desired state
  containers:                         # List of containers in the Pod
    - name: app                       # Name of the container
      image: nginx                    # Container image to use (Nginx web server)
      volumeMounts:                   # Mount points for volumes inside the container
        - mountPath: /usr/share/nginx/html # Path in the container where the volume is mounted
          name: web-content             # Name of the volume to mount (matches volume definition)
  volumes:                            # List of volumes available to the Pod
    - name: web-content               # Name of the volume
      persistentVolumeClaim:          # Specifies that the volume is backed by a PVC
        claimName: dynamic-pvc        # Name of the PVC to bind to
```

---

## 4. 🔹 Generic Ephemeral Volume
- No separate PVC object needed
- Persistent across container restarts (not across Pod deletion)
- Great for simple ephemeral but persistent storage

```yaml
apiVersion: v1                        # Specifies the Kubernetes API version for Pods
kind: Pod                             # Defines the resource type as a Pod
metadata:                             # Metadata section for the Pod
  name: generic-ephemeral-pod         # Name of the Pod
spec:                                 # Specification for the Pod's desired state
  containers:                         # List of containers in the Pod
    - name: app                       # Name of the container
      image: nginx                    # Container image to use (Nginx web server)
      volumeMounts:                   # Mount points for volumes inside the container
        - mountPath: /data              # Path in the container where the volume is mounted
          name: my-ephemeral            # Name of the volume to mount (matches volume definition)
  volumes:                            # List of volumes available to the Pod
    - name: my-ephemeral              # Name of the volume
      ephemeral:                      # Defines an ephemeral volume
        volumeClaimTemplate:          # Template for creating a PVC-like volume
          metadata:                   # Metadata for the volume
            labels:                   # Labels applied to the volume
              type: generic           # Label to identify the volume type
          spec:                       # Specification for the volume
            accessModes: [ "ReadWriteOnce" ] # Requests read/write access by a single node
            resources:                # Resource requirements for the volume
              requests:               # Specifies the minimum resources needed
                storage: 1Gi          # Requests 1 gibibyte of storage
```

---

## 5. 🔹 StatefulSet with VolumeClaimTemplates
- Perfect for stateful apps like databases
- Automatically creates one PVC per replica
- Uses the default StorageClass

```yaml
apiVersion: apps/v1                   # Specifies the Kubernetes API version for StatefulSets
kind: StatefulSet                     # Defines the resource type as a StatefulSet
metadata:                             # Metadata section for the StatefulSet
  name: postgres                      # Name of the StatefulSet
spec:                                 # Specification for the StatefulSet's desired state
  serviceName: "postgres"             # Name of the headless Service for Pod DNS resolution
  replicas: 2                         # Number of Pod replicas to maintain
  selector:                           # Selector to match Pods managed by the StatefulSet
    matchLabels:                      # Labels to match Pods
      app: postgres                   # Label key-value pair to identify Pods
  template:                           # Template for creating Pods
    metadata:                         # Metadata for the Pods
      labels:                         # Labels applied to the Pods
        app: postgres                 # Label to identify the Pods
    spec:                             # Specification for the Pods
      containers:                     # List of containers in each Pod
        - name: postgres              # Name of the container
          image: postgres:14          # Container image to use (PostgreSQL 14)
          volumeMounts:               # Mount points for volumes inside the container
            - name: data              # Name of the volume to mount
              mountPath: /var/lib/postgresql/data # Path in the container for PostgreSQL data
  volumeClaimTemplates:               # Template for creating PVCs for each Pod
    - metadata:                       # Metadata for the PVC
        name: data                    # Name of the PVC (used in volumeMounts)
      spec:                           # Specification for the PVC
        accessModes: [ "ReadWriteOnce" ] # Requests read/write access by a single node
        resources:                    # Resource requirements for the PVC
          requests:                   # Specifies the minimum resources needed
            storage: 1Gi              # Requests 1 gibibyte of storage
        storageClassName: microk8s-hostpath # Specifies the StorageClass for dynamic provisioning
```

---

# 📊 Summary Table

| Volume Type                             | Manual PV | Manual PVC | Use Case                              |
|----------------------------------------|-----------|------------|----------------------------------------|
| `emptyDir`                             | ❌        | ❌         | Temp files, cache, ephemeral storage   |
| `PersistentVolume + PersistentVolumeClaim` | ✅        | ✅         | Full manual control over storage       |
| `PVC only (Dynamic with StorageClass)` | ❌        | ✅         | Dynamic provisioning, easy to use      |
| `Generic Ephemeral Volume`             | ❌        | ❌         | Pod-level inline persistent storage    |
| `StatefulSet + VolumeClaimTemplates`   | ❌        | ❌         | Per-replica volumes, databases, stateful apps |

---