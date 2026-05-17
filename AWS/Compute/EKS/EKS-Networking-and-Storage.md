# EKS Networking & Storage

Understanding how EKS integrates with native AWS networking and storage solutions is crucial for running stateful and secure production-grade workloads.

## 4. Networking & CNI

### Amazon VPC CNI Plugin
The native networking plugin for EKS that assigns a real, private IP address from your AWS VPC directly to every single Pod, optimizing network performance and security group integration.

- **How it works**: In traditional Kubernetes, pods get an IP address from an overlay network (like Flannel or Calico), which requires packet encapsulation. In EKS, the Amazon VPC CNI plugin automatically provisions Elastic Network Interfaces (ENIs) on your worker nodes and assigns secondary IP addresses from those ENIs directly to your pods.
- **Benefits**: 
  - **High Performance**: Eliminates the overhead of network encapsulation and decapsulation, resulting in native VPC network performance.
  - **Native Integration**: Because pods have real VPC IPs, they can communicate directly with other AWS services (like RDS, ElastiCache, or on-premises resources via Transit Gateway).
  - **Security**: You can leverage "Security Groups for Pods" to assign specific AWS Security Groups directly to individual pods, enforcing strict network isolation at the pod level rather than the node level.

**CLI Commands / Add-on Management:**
```bash
# The CNI plugin runs as a DaemonSet named 'aws-node' on every worker node
kubectl get daemonset aws-node -n kube-system

# EKS allows you to manage the CNI plugin as a managed Add-on
aws eks update-addon \
    --cluster-name my-eks-cluster \
    --addon-name vpc-cni \
    --addon-version v1.15.0-eksbuild.1 \
    --resolve-conflicts PRESERVE
```

## 5. Storage Provisioning

### CSI Drivers (EBS & EFS)
Container Storage Interface (CSI) plug-ins that allow EKS pods to dynamically provision and attach persistent, network-attached AWS storage (EBS block storage or shared EFS file systems).

- **Amazon EBS CSI Driver**:
  - Provides **ReadWriteOnce** access (a volume can only be mounted to a single node at a time).
  - Ideal for stateful applications like databases (PostgreSQL, MongoDB) that require high-performance, low-latency block storage.
  - **Dynamic Provisioning**: When a Kubernetes `PersistentVolumeClaim` (PVC) is created, the CSI driver automatically provisions an underlying AWS EBS volume, attaches it to the correct EC2 worker node, and formats it for the pod.
- **Amazon EFS CSI Driver**:
  - Provides **ReadWriteMany** access (a volume can be mounted by hundreds of pods across different worker nodes and Availability Zones simultaneously).
  - Ideal for shared applications, content management systems (like WordPress), or distributed machine learning workloads that need shared access to the same filesystem.

**CLI Commands / Manifests:**
```bash
# Check if the EBS CSI driver pods are running in your cluster
kubectl get pods -n kube-system -l "app.kubernetes.io/name=aws-ebs-csi-driver"

# Example of dynamically provisioning an EBS volume using a PersistentVolumeClaim (PVC).
# This assumes an EBS-backed StorageClass named 'ebs-sc' exists.
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 20Gi
EOF

# Verify that the persistent volume was successfully created and bound
kubectl get pvc
```
