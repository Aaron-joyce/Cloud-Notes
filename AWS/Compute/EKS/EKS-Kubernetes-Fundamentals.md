# Kubernetes Fundamentals in EKS

While Amazon EKS provides the managed infrastructure, you still interact with it using standard Kubernetes constructs. Here are the core fundamentals you deploy to your EKS clusters.

## 3. Kubernetes Fundamentals

### Pods
The smallest, basic deployable objects in Kubernetes that wrap one or more tightly coupled containers sharing storage and network resources.

- **How it works**: A pod represents a single instance of a running process in your cluster. If you have a web application and a logging sidecar, they often run together inside a single pod. Containers within the same pod share an IP address and port space (localhost).
- **In EKS**: EKS pods get native AWS VPC IP addresses (if using the Amazon VPC CNI plugin), meaning each pod functions as a first-class citizen on your AWS network, able to communicate directly with other AWS services.

**CLI Commands:**
```bash
# View running pods in the current namespace
kubectl get pods

# View pods across all namespaces with extra details (like node placement and IP)
kubectl get pods --all-namespaces -o wide

# Describe a specific pod to view its configurations and event history (useful for debugging)
kubectl describe pod my-web-pod
```

### Deployments & ReplicaSets
Declarative manifests that define the desired state, scaling limits, and update strategies for a set of identical Pods.

- **ReplicaSet**: A low-level controller that ensures a specified number of identical pod replicas are running at any given time.
- **Deployment**: A higher-level concept that manages ReplicaSets. It provides declarative updates to pods. If you change a Deployment's container image, it creates a new ReplicaSet, scales it up, and slowly scales down the old one (Rolling Update).
- **Benefits**: Self-healing. If an underlying EC2 worker node goes down and its pods are lost, the Deployment/ReplicaSet automatically schedules replacement pods on available nodes to maintain the desired count.

**CLI Commands:**
```bash
# Create a deployment imperatively
kubectl create deployment my-nginx --image=nginx:latest --replicas=3

# Scale a deployment manually
kubectl scale deployment my-nginx --replicas=5

# View the rollout status during an update
kubectl rollout status deployment/my-nginx

# View active deployments
kubectl get deployments
```

### Services & Ingress
Kubernetes network resources used to expose a logical set of Pods as a network service internally (ClusterIP/NodePort) or route external HTTP/HTTPS traffic to them (Ingress).

- **Services**: Because Pod IPs are ephemeral (they change when a pod is destroyed and recreated), a Service provides a stable, static IP and DNS name to access a group of pods.
  - *ClusterIP*: Exposes the service on a cluster-internal IP (only reachable from within the cluster).
  - *NodePort*: Exposes the service on each Node's IP at a static port.
  - *LoadBalancer*: In EKS, setting this type automatically provisions an AWS Network Load Balancer (NLB) or Classic Load Balancer to expose the service to the internet.
- **Ingress**: Manages external access to the services in a cluster, providing L7 HTTP/HTTPS routing. In EKS, by installing the AWS Load Balancer Controller, creating an Ingress object automatically provisions an AWS Application Load Balancer (ALB) to route traffic based on URL paths or hostnames.

**CLI Commands:**
```bash
# Expose an existing deployment as a LoadBalancer service
kubectl expose deployment my-nginx --port=80 --target-port=80 --type=LoadBalancer

# View services and their external IPs/DNS endpoints
kubectl get svc

# View ingress resources
kubectl get ingress
```
