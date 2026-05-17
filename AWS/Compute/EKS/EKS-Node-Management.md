# EKS Node Management & Data Plane Options

When running applications on Amazon EKS, you have several options for managing the underlying compute infrastructure (the data plane) where your Kubernetes pods are scheduled.

## 2. Node Management & Data Plane Options

### Managed Node Groups
An EKS feature that automates the provisioning, scaling, and lifecycle management (including OS patching and updates) of EC2 worker nodes.

- **How it works**: EKS handles the heavy lifting of keeping your nodes secure and up-to-date. Nodes are run using Amazon EC2 Auto Scaling groups managed on your behalf by AWS.
- **Benefits**: Seamless integration with the Kubernetes Cluster Autoscaler. You can update an entire node group to a new AMI or Kubernetes version with a single API call or console click without disrupting running applications (EKS automatically cordons and drains nodes gracefully before terminating them).

**CLI Commands:**
```bash
# Create a managed node group with specific instance types
aws eks create-nodegroup \
    --cluster-name my-eks-cluster \
    --nodegroup-name standard-workers \
    --node-role arn:aws:iam::123456789012:role/NodeInstanceRole \
    --subnets subnet-12345 subnet-67890 \
    --instance-types t3.medium \
    --scaling-config minSize=2,maxSize=5,desiredSize=2

# Update the node group (e.g., triggering a rolling update to a new Kubernetes version)
aws eks update-nodegroup-version \
    --cluster-name my-eks-cluster \
    --nodegroup-name standard-workers \
    --kubernetes-version 1.28
```

### Self-Managed Nodes
Custom EC2 instances that you manually provision, configure, and register to the EKS cluster, giving you absolute control over OS and runtime configurations.

- **How it works**: You are responsible for launching the EC2 instances (usually via CloudFormation, Terraform, or your own Auto Scaling Groups), installing the `kubelet`, configuring it to point to the EKS API server, and handling all OS updates and AMI rotations yourself.
- **Use Case**: Necessary when you have strict requirements that Managed Node Groups cannot meet, such as highly customized, proprietary AMIs, specific edge-case networking setups, or legacy configurations.

**CLI / Config Details:**
```bash
# Self-managed nodes are usually launched via infrastructure-as-code.
# The user data script of the EC2 instance must execute the EKS bootstrap script 
# to join the cluster:
#!/bin/bash
set -o xtrace
/etc/eks/bootstrap.sh my-eks-cluster
```

### AWS Fargate with EKS
A serverless approach where EKS provisions a dedicated, isolated compute environment for every single Kubernetes Pod, removing the need to manage underlying worker nodes.

- **How it works**: You define a Fargate Profile that matches specific pod labels or namespaces. When a pod matching that profile is created, EKS automatically provisions the exact compute capacity (CPU and Memory) needed for that specific pod.
- **Benefits**: Zero EC2 instances to manage, patch, or scale. Built-in security through hypervisor-level isolation for every pod. Pricing is calculated strictly per pod based on its requested vCPU and memory.

**CLI Commands:**
```bash
# Create a Fargate profile targeting a specific namespace
aws eks create-fargate-profile \
    --fargate-profile-name my-fargate-profile \
    --cluster-name my-eks-cluster \
    --pod-execution-role-arn arn:aws:iam::123456789012:role/AmazonEKSFargatePodExecutionRole \
    --subnets subnet-12345 subnet-67890 \
    --selectors namespace=serverless-apps
```

### EKS Hybrid / Anywhere
Solutions for running and managing consistent, open-source Kubernetes clusters on your own physical, on-premises infrastructure.

- **EKS Anywhere**: Allows you to create and operate Kubernetes clusters on your own on-premises infrastructure (VMware vSphere, bare metal, etc.) using the exact same open-source Kubernetes distribution (Amazon EKS Distro) used by EKS in the cloud.
- **EKS Connector**: A feature that allows you to connect any conformant Kubernetes cluster (including those on-premises or in other clouds) to the EKS console, giving you a central dashboard to view all your clusters.
- **Benefits**: Consistent tooling, consistent Kubernetes versions, and a unified management pane regardless of where the compute actually lives.

**CLI Commands:**
```bash
# EKS Anywhere clusters are typically created using the eksctl anywhere plugin:
eksctl anywhere create cluster -f my-cluster-config.yaml
```
