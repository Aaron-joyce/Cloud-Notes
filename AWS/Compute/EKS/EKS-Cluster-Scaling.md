# EKS Cluster Scaling

Effectively scaling applications on Amazon EKS involves two main layers: scaling the applications (the pods) and scaling the underlying infrastructure (the EC2 nodes) to accommodate those pods.

## 6. Pod Scaling

### Horizontal Pod Autoscaler (HPA)
The native Kubernetes mechanism that dynamically scales the number of Pods in a deployment based on observed CPU/memory utilization or custom metrics.

- **How it works**: The HPA controller continuously monitors the metrics of a workload (usually via the Kubernetes Metrics Server). If a workload exceeds a defined threshold (e.g., 70% average CPU), the HPA updates the `ReplicaSet` to increase the pod count. Once the load drops, it gracefully scales the pods back down.
- **Dependencies**: Requires the Kubernetes Metrics Server to be installed in the cluster to provide standard CPU and memory metrics.

**CLI Commands / Manifests:**
```bash
# Imperatively create an HPA for an existing deployment, maintaining 50% CPU usage
kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10

# View active HPAs and their current metrics
kubectl get hpa

# Example HPA Declarative Manifest
cat <<EOF | kubectl apply -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
EOF
```

## 7. Node Scaling

When the HPA asks for more pods, but your current worker nodes don't have enough spare CPU/Memory to schedule them, the new pods sit in a `Pending` state. You must scale the underlying EC2 nodes to resolve this.

### Cluster Autoscaler vs. Karpenter

**1. Cluster Autoscaler**
The traditional choice for group-based node scaling.
- **How it works**: It monitors the cluster for `Pending` pods. When it detects them, it makes an API call to the AWS Auto Scaling Group (ASG) associated with your Managed Node Group to increase the desired capacity, which launches a new EC2 instance.
- **Pros**: Mature, highly stable, and relies on standard AWS ASGs.
- **Cons**: Slower to provision nodes. You must manage statically defined Node Groups, which limits flexibility (e.g., you need separate groups for x86 vs. ARM instances, or On-Demand vs. Spot).

**2. Karpenter**
A high-performance, just-in-time Kubernetes cluster autoscaler built by AWS that provisions optimally sized nodes instantly based on pending Pod requirements.
- **How it works**: Karpenter bypasses AWS Auto Scaling Groups entirely. It watches for `Pending` pods, analyzes their specific resource requirements (CPU, memory, GPU, node affinities), and calls the Amazon EC2 Fleet API directly to launch a custom-fit, optimal EC2 instance in seconds.
- **Pros**: 
  - **Speed**: Provisions nodes incredibly fast (often under a minute).
  - **Cost-efficiency**: It can automatically consolidate workloads onto fewer, cheaper nodes over time.
  - **Flexibility**: No need to manage dozens of static node groups; Karpenter mixes and matches instance types dynamically based on immediate needs.
- **Cons**: Requires giving the Karpenter controller extensive IAM permissions to manage EC2 instances directly on your behalf.

**CLI Commands / Manifests (Karpenter example):**
```bash
# View Karpenter logs to watch it make real-time provisioning decisions
kubectl logs -f -n karpenter -l app.kubernetes.io/name=karpenter

# Example Karpenter Provisioner Manifest
# It dynamically selects instance types based on the pod's needs, favoring Spot instances
cat <<EOF | kubectl apply -f -
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: default
spec:
  requirements:
    - key: karpenter.sh/capacity-type
      operator: In
      values: ["spot", "on-demand"]
  providerRef:
    name: default
  ttlSecondsAfterEmpty: 30 # Instantly terminates the node if it remains empty for 30 seconds
EOF
```
