# EKS Security and Identity

Securing an Amazon EKS cluster involves managing who can interact with the cluster's API (Authentication & Authorization) and what AWS resources the applications running inside the cluster are allowed to access (Pod Permissions).

## 8. Security & Identity

### AWS IAM Authenticator / RBAC
The authentication bridge that uses AWS IAM to authenticate a user’s identity, while utilizing native Kubernetes Role-Based Access Control (RBAC) to authorize actions inside the cluster.

- **Authentication (Who are you?)**: When a developer or CI/CD pipeline runs a `kubectl` command, the AWS IAM Authenticator passes an IAM identity token to the EKS API server. EKS validates this token against AWS IAM to confirm the caller's identity.
- **Authorization (What can you do?)**: Once the identity is confirmed, the IAM User or Role ARN must be mapped to a Kubernetes User or Group. Kubernetes RBAC (`Roles`, `ClusterRoles`, `RoleBindings`) then dictates what that mapped identity is actually allowed to do (e.g., read pods in the `dev` namespace, or delete deployments cluster-wide).

**CLI Commands / Manifests:**
```bash
# EKS historically used the 'aws-auth' ConfigMap to map IAM ARNs to Kubernetes groups.
# (Note: In newer EKS versions, EKS Access Entries provide a fully API-driven alternative to this ConfigMap).
kubectl describe configmap aws-auth -n kube-system

# Example RoleBinding granting a specific mapped group "edit" access to a namespace
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-edit-binding
  namespace: my-app-ns
subjects:
- kind: Group
  name: my-developer-group # This maps to the group defined in IAM mapping
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: edit
  apiGroup: rbac.authorization.k8s.io
EOF
```

### EKS Pod Identity
The modern, secure mechanism that maps AWS IAM roles directly to Kubernetes ServiceAccounts, granting individual Pods granular permissions to access AWS services.

- **How it works**: Before EKS Pod Identity, EKS relied on IAM Roles for Service Accounts (IRSA) which required setting up OIDC providers. EKS Pod Identity greatly simplifies this. You install the EKS Pod Identity Agent add-on to your cluster. When a pod needs to call an AWS service (e.g., querying DynamoDB), the agent transparently securely provides the temporary AWS credentials associated with the IAM role you mapped to the pod's Kubernetes ServiceAccount.
- **Benefits**: 
  - **Granular Security**: Follows the principle of least privilege. Instead of giving broad IAM permissions to the underlying EC2 worker node (which all pods on that node could abuse), you give exact permissions *only* to the specific pod that needs them.
  - **Simplicity**: Eliminates the need to manage OIDC provider configurations or manually annotate Kubernetes service accounts.

**CLI Commands / Manifests:**
```bash
# Create an EKS Pod Identity mapping between an IAM role and a Kubernetes ServiceAccount
aws eks create-pod-identity-association \
    --cluster-name my-eks-cluster \
    --namespace my-app-ns \
    --service-account my-app-sa \
    --role-arn arn:aws:iam::123456789012:role/MyAppDynamoDBAccessRole

# Example Pod specifying the linked ServiceAccount
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  namespace: my-app-ns
spec:
  serviceAccountName: my-app-sa # The pod inherits the IAM role mapped to this SA
  containers:
  - name: my-app-container
    image: my-app-image:latest
EOF
```
