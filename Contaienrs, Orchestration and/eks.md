This is a comprehensive guide to recreating the **Event-Driven Image Processor** on EKS. This Markdown document covers the entire lifecycle from cluster creation to the common "Free Tier" pitfalls we encountered.

---

# AWS EKS Image Processor: Step-by-Step Deployment Guide

This guide details how to deploy a Python-based image processing microservice on **Amazon EKS** using `eksctl`. The service listens for S3 uploads, generates thumbnails, and logs metadata to DynamoDB.


## 1. EKS Cluster Creation

### The "One-Shot" Cluster Command
Use `eksctl` to provision the Control Plane and Managed Node Group simultaneously. 

> **Note on Free Tier:** For Free Tier eligibility in regions like Mumbai, use `t3.small` or `t3.micro`. `t3.small` is recommended for EKS to avoid resource exhaustion.

```bash
eksctl create cluster \
  --name <CLUSTER_NAME> \
  --region <REGION> \
  --nodegroup-name <NODEGROUP_NAME> \
  --node-type <INSTANCE_TYPE> \
  --nodes <NODE_COUNT> \
  --with-oidc \
  --managed
```
* `<CLUSTER_NAME>`: Name of your EKS cluster (e.g., `eks-practice`).
* `<INSTANCE_TYPE>`: Use `t3.small` for a balance of cost and performance.
* `<NODE_COUNT>`: Recommended `2` or `3` for high availability.

### IAM Service Account (IRSA)
To allow Pods to access S3 and DynamoDB without using hardcoded credentials, create an IAM Service Account.

```bash
eksctl create iamserviceaccount \
  --name <SERVICE_ACCOUNT_NAME> \
  --cluster <CLUSTER_NAME> \
  --region <REGION> \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess \
  --approve
```
* `<SERVICE_ACCOUNT_NAME>`: The name referenced in your YAML (e.g., `s3-dynamo-sa`).

---

## 2. Container Management (ECR)

### Push Image to ECR
```bash
# Login to ECR
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

# Build and Tag
docker build -t <IMAGE_NAME> .
docker tag <IMAGE_NAME>:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE_NAME>:latest

# Push
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE_NAME>:latest
```
* `<AWS_ACCOUNT_ID>`: Your 12-digit AWS Account ID.
* `<IMAGE_NAME>`: The name of your Docker repository (e.g., `image-proc`).

---

## 3. Kubernetes Deployment configuration

### `deployment.yaml` Syntax
Ensure the `selector` labels match the `template` labels exactly.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <DEPLOYMENT_NAME>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <APP_LABEL>
  template:
    metadata:
      labels:
        app: <APP_LABEL>
    spec:
      serviceAccountName: <SERVICE_ACCOUNT_NAME>
      containers:
      - name: <CONTAINER_NAME>
        image: <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE_NAME>:latest
        imagePullPolicy: Always
        env:
        - name: SOURCE_BUCKET
          value: "<SOURCE_BUCKET_NAME>"
        - name: DEST_BUCKET
          value: "<DEST_BUCKET_NAME>"
        - name: DYNAMO_TABLE
          value: "<DYNAMO_TABLE_NAME>"
        - name: REGION_NAME
          value: "<REGION>"
```

---

## 4. Troubleshooting & Error Cases

| Error Message | Cause | Resolution |
| :--- | :--- | :--- |
| `AlreadyExistsException` | The CloudFormation stack already exists from a previous failed/timed-out run. | Run `eksctl utils write-kubeconfig --cluster <CLUSTER_NAME>` to re-link, or delete the stack and restart. |
| `selector` does not match template `labels` | The labels in `spec.selector.matchLabels` and `spec.template.metadata.labels` are different. | Update the YAML so both blocks use the exact same key-pair (e.g., `app: processor`). |
| `Pending` Status (No Nodes) | EC2 instances haven't joined the cluster yet or failed to launch. | Check `kubectl get nodes`. If empty, check the **Auto Scaling Group** "Activity" tab in the EC2 Console. |
| `ImagePullBackOff` | Kubernetes cannot find the image in ECR. | Verify the Image URI in the YAML. Ensure there are no spaces in the URL string. |
| `found character that cannot start any token` | Invalid YAML syntax, usually a hidden tab character or a trailing space after a value. | Open file in `nano`, delete the line, and re-type it manually using only spaces for indentation. |
| `UpdateTerminationProtection` error during delete | `eksctl` cannot delete the stack because it is protected. | Go to CloudFormation Console -> Stack Actions -> **Disable Termination Protection**, then delete. |

---

## 5. Cleanup (Avoid Unwanted Charges)
```bash
# 1. Delete Cluster (Nodes, VPC, and Control Plane)
eksctl delete cluster --name <CLUSTER_NAME> --region <REGION>
```