# AWS Identity and Access Management (IAM) & Access Control

AWS IAM enables you to securely manage access to AWS services and resources.

## 1. Identities & Authentication Primitives

### Root User Protection and Multi-Factor Authentication (MFA)
The Root User is the account owner with absolute access. It should be heavily protected with a strong password and hardware MFA, and never used for day-to-day operations.

### IAM Users and Long-Term Access Keys
- **IAM Users**: Distinct identities created within your AWS account that represent the people or applications interacting with AWS.
- **Access Keys**: Long-term credentials (Access Key ID and Secret Access Key) used for programmatic access to AWS APIs.

### IAM Groups and Group-Based Policy Assignment
Groups are collections of IAM Users. You can specify permissions for multiple users by attaching policies to the group, which simplifies access management.

### IAM Roles and Cross-Account Trust Relationships
- **IAM Roles**: Identities that can be assumed by anyone who needs it. Roles do not have standard long-term credentials; instead, they provide temporary security credentials.
- **Cross-Account Trust**: Roles can be configured to trust other AWS accounts, allowing users or services in those accounts to assume the role.

### AWS Identity Center (Successor to AWS Single Sign-On)
The recommended central hub to manage workforce access to multiple AWS accounts and cloud applications. It integrates with your existing corporate directory (like Active Directory or Okta).

## 2. Policy Types & Evaluation Logic

### Identity-Based Policies
Attached to IAM users, groups, or roles.
- **Managed Policies**: Standalone policies created and administered by AWS or the customer that can be attached to multiple identities.
- **Inline Policies**: Policies that are strictly embedded directly into a single IAM identity.

### Resource-Based Policies
Attached directly to an AWS resource (e.g., S3 Bucket Policies, KMS Key Policies, SQS Queue Policies) to dictate who has access to the resource.

### Permissions Boundaries
An advanced feature that allows you to set the maximum permissions that an identity-based policy can grant to an IAM entity.

### AWS Organizations Service Control Policies (SCPs)
Policies that offer central control over the maximum available permissions for all accounts in your AWS Organization. They do not grant permissions; they only restrict them.

### IAM Policy Evaluation Order
When an API request is made, AWS evaluates permissions in the following order:
1. Explicit Deny
2. Service Control Policy (SCP)
3. Resource Policy
4. Permissions Boundary
5. Identity Policy
6. Implicit Deny (Default state if no explicit Allow is found)

## 3. Advanced Access Controls & Auditing

### Attribute-Based Access Control (ABAC)
An authorization strategy that defines permissions based on attributes (tags). You can create IAM policies that allow operations only when the principal's tags match the resource's tags.

### IAM Access Analyzer
A tool that helps you identify resources in your organization and accounts, such as Amazon S3 buckets or IAM roles, that are shared with an external entity. It validates policies against IAM best practices.

### IAM Credential Report & Access Advisor
- **Credential Report**: Lists all users in an account and the status of their various credentials (passwords, access keys, MFA).
- **Access Advisor**: Shows the service permissions granted to a user and when those services were last accessed, helping you remove unused permissions.
