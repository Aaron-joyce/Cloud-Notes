# Amazon EKS IAM Policy Guide

Amazon EKS relies on IAM for authenticating to the cluster API (via the AWS IAM Authenticator) and for granting pods access to AWS resources (via EKS Pod Identity or IRSA).

## Common Use Cases & Required Permissions

### 1. Cluster Read-Only Access
Allows a user to view EKS clusters in the console and get the cluster configuration.
* **Required Actions**: `eks:DescribeCluster`, `eks:ListClusters`

### 2. EKS Cluster Administrator
Allows creating and deleting clusters, managing node groups, and configuring add-ons.
* **Required Actions**: 
  * `eks:CreateCluster`, `eks:DeleteCluster`
  * `eks:CreateNodegroup`, `eks:DeleteNodegroup`
  * `iam:PassRole` (To pass the cluster role and node instance roles)

*Sample Snippet (Connecting to a cluster with kubectl):*
```json
{
  "Effect": "Allow",
  "Action": "eks:DescribeCluster",
  "Resource": "arn:aws:eks:us-east-1:123456789012:cluster/my-cluster"
}
```
*(Note: To actually execute `kubectl get pods`, the IAM identity must ALSO be mapped inside the cluster's RBAC system).*

## Sample Policy: Manage EKS Pod Identity
This policy allows an administrator to manage EKS Pod Identity associations, mapping IAM roles directly to Kubernetes Service Accounts without allowing them to delete the actual cluster.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ViewEKSAndIAM",
      "Effect": "Allow",
      "Action": [
        "eks:DescribeCluster",
        "eks:ListClusters",
        "iam:ListRoles"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ManagePodIdentities",
      "Effect": "Allow",
      "Action": [
        "eks:CreatePodIdentityAssociation",
        "eks:UpdatePodIdentityAssociation",
        "eks:DeletePodIdentityAssociation",
        "eks:DescribePodIdentityAssociation",
        "eks:ListPodIdentityAssociations"
      ],
      "Resource": "arn:aws:eks:*:*:cluster/my-cluster"
    },
    {
      "Sid": "PassRoleToEKSPods",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::*:role/*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "pods.eks.amazonaws.com"
        }
      }
    }
  ]
}
```
