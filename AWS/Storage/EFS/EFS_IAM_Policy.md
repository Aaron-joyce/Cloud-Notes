# Amazon EFS IAM Policy Guide

IAM in EFS is used to control who can create/delete file systems and who can mount them. EFS also supports resource-based policies (File System Policies) similar to S3.

## Common Use Cases & Required Permissions

### 1. Client Mount Access
Controls whether an EC2 instance or Lambda function is allowed to mount the file system.
* **Required Actions**: `elasticfilesystem:ClientMount`, `elasticfilesystem:ClientWrite`

*Sample Snippet (Allowing read-only mount):*
```json
{
  "Effect": "Allow",
  "Action": "elasticfilesystem:ClientMount",
  "Resource": "arn:aws:elasticfilesystem:us-east-1:123456789012:file-system/fs-12345678"
}
```

## Sample Policy: Enforce Encryption on Mount (Resource Policy)
This is typically attached to the EFS File System itself (Resource-Based Policy), preventing any client from connecting unless they use TLS encryption.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "elasticfilesystem:ClientMount",
      "Resource": "arn:aws:elasticfilesystem:us-east-1:123456789012:file-system/fs-12345678",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```
