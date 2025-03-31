# Why Kubernetes?

Docker allows you to create and run containers, but when you have multiple containers across multiple machines, managing them manually becomes a challenge. This is where Kubernetes (K8s) comes in.

## Problems Kubernetes Solves:
1. **Container Orchestration**  
   - Running multiple containers across different machines is hard to manage manually.  
   - Kubernetes automates the deployment, scaling, and management of containerized applications.

2. **Auto-Scaling**  
   - Docker containers do not auto-scale on their own.  
   - Kubernetes can automatically scale containers up or down based on CPU, memory, or custom metrics.

3. **Load Balancing**  
   - A single container instance cannot handle high traffic.  
   - Kubernetes distributes traffic across multiple containers to balance the load.

4. **Self-Healing**  
   - If a container crashes, Docker does not restart it automatically.  
   - Kubernetes detects failures and restarts unhealthy containers.

5. **Service Discovery & Networking**  
   - With multiple containers running, how do they communicate?  
   - Kubernetes provides built-in networking and service discovery.

6. **Configuration Management & Secrets Handling**  
   - Managing environment variables, database credentials, and API keys securely is challenging.  
   - Kubernetes provides **ConfigMaps** and **Secrets** to manage configurations securely.

7. **Storage Orchestration**  
   - Containers are stateless by default. What happens to data if a container restarts?  
   - Kubernetes provides **Persistent Volumes (PV)** and **Persistent Volume Claims (PVC)** to manage storage.

---

# Basics of Kubernetes

## 1. Kubernetes Architecture
Kubernetes is made up of the following key components:

- **Master Node (Control Plane)**: Manages the cluster and makes scheduling decisions.
- **Worker Nodes**: Run the application workloads (containers).
- **Kubelet**: An agent on each worker node that ensures the containers are running.
- **Pod**: The smallest unit in Kubernetes that contains one or more containers.
- **Service**: Exposes a set of Pods to other applications or users.
- **Ingress**: Manages external access to services (e.g., HTTP/HTTPS).
- **ConfigMap & Secret**: Store configuration data securely.
- **Persistent Volume (PV) & Persistent Volume Claim (PVC)**: Manage storage for stateful applications.

## 2. Key Kubernetes Objects
| Object | Description |
|--------|-------------|
| **Pod** | The smallest deployable unit containing one or more containers. |
| **Deployment** | Manages multiple replica Pods for scaling and updates. |
| **Service** | Exposes Pods internally (ClusterIP) or externally (LoadBalancer, NodePort). |
| **ConfigMap** | Stores configuration data for applications. |
| **Secret** | Stores sensitive data like passwords securely. |
| **Ingress** | Manages HTTP and HTTPS access to services. |
| **Persistent Volume (PV)** | Provides persistent storage. |
| **Persistent Volume Claim (PVC)** | Requests storage from PVs. |
| **Namespace** | Logical grouping of resources. |

## 3. Kubernetes Workflow (How Applications Run)
1. **Write a YAML file** defining Pods, Deployments, and Services.
2. **Apply the YAML file** using `kubectl apply -f <file>.yaml`.
3. **Kubernetes schedules the Pod** on a suitable worker node.
4. **Kubelet ensures** the Pod is running and healthy.
5. **Services and Ingress** expose the application.
6. **Auto-scaling and self-healing** ensure high availability.

## 4. Basic Kubernetes Commands
- Check cluster nodes:  
  ```bash
  kubectl get nodes
  ```
- Deploy an application:  
  ```bash
  kubectl apply -f deployment.yaml
  ```
- List running pods:  
  ```bash
  kubectl get pods
  ```
- Get details of a pod:  
  ```bash
  kubectl describe pod <pod-name>
  ```
- Delete a resource:  
  ```bash
  kubectl delete -f deployment.yaml
  ```

