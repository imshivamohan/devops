
# 📦 Kubernetes Storage Cheat Sheet

## 1. 🔹 emptyDir
- Ephemeral storage tied to Pod lifecycle
- Data is deleted when the Pod is removed
- Great for caching, temp files

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-pod
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: /tmp/cache
          name: temp-storage
  volumes:
    - name: temp-storage
      emptyDir: {}
```

---

## 2. 🔹 PersistentVolume (PV) + PersistentVolumeClaim (PVC)
- Manually create the PV and the PVC
- Useful for fine-grained control
- Good for hostPath, NFS, or fixed resources

```yaml
# PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"

---
# PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

## 3. 🔹 PVC Only (Dynamic Provisioning with StorageClass)
- PVC triggers PV creation dynamically
- No need to create PV manually
- Uses the default StorageClass (like `microk8s-hostpath`)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: microk8s-hostpath
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dynamic-pod
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: /usr/share/nginx/html
          name: web-content
  volumes:
    - name: web-content
      persistentVolumeClaim:
        claimName: dynamic-pvc
```

---

## 4. 🔹 Generic Ephemeral Volume
- No separate PVC object needed
- Persistent across container restarts (not across Pod deletion)
- Great for simple ephemeral but persistent storage

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: generic-ephemeral-pod
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: /data
          name: my-ephemeral
  volumes:
    - name: my-ephemeral
      ephemeral:
        volumeClaimTemplate:
          metadata:
            labels:
              type: generic
          spec:
            accessModes: [ "ReadWriteOnce" ]
            resources:
              requests:
                storage: 1Gi
```

---

## 5. 🔹 StatefulSet with VolumeClaimTemplates
- Perfect for stateful apps like databases
- Automatically creates one PVC per replica
- Uses the default StorageClass

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"
  replicas: 2
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:14
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 1Gi
        storageClassName: microk8s-hostpath
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

