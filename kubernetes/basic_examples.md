# Basic Kubernetes Examples

This document contains YAML examples for fundamental Kubernetes components.

---

## 1. Pod Example (`pod.yaml`)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: nginx-container
      image: nginx
      ports:
        - containerPort: 80
```
Creates a single Nginx container inside a Pod.

---

## 2. Deployment Example (`deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: nginx-container
          image: nginx
          ports:
            - containerPort: 80
```
Creates 3 replicas of the Pod and ensures high availability.

---

## 3. Service Example (`service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP  # Change to LoadBalancer or NodePort for external access
```
Exposes the Pods internally using a stable IP.

---

## 4. ConfigMap Example (`configmap.yaml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
```
Stores environment variables for the application.

---

## 5. Secret Example (`secret.yaml`)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  DB_PASSWORD: bXlTdXBlclBhc3M=  # Base64 encoded "mySuperPass"
```
Stores sensitive information securely.

---

## 6. Persistent Volume & Persistent Volume Claim (`pv-pvc.yaml`)
```yaml
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
Creates persistent storage for stateful apps.

---

## 7. Ingress Example (`ingress.yaml`)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```
Routes external traffic (myapp.local) to the internal service.

---

## 8. Applying All YAML Files
Run the following commands to apply all components:
```bash
kubectl apply -f pod.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f pv-pvc.yaml
kubectl apply -f ingress.yaml
```

This covers all key Kubernetes components in a simple way.

