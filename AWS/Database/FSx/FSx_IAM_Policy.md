# Amazon FSx IAM Policy Guide

IAM permissions for FSx control the management of the file systems (creation, deletion, backups). Data access is typically controlled by the underlying file system protocol (e.g., Active Directory for Windows, POSIX for Lustre).

## Common Use Cases & Required Permissions

### 1. FSx Administrator
Allows managing the lifecycle of the file systems and their backups.
* **Required Actions**: `fsx:CreateFileSystem`, `fsx:DeleteFileSystem`, `fsx:CreateBackup`, `fsx:Describe*`

*Sample Snippet (Creating backups):*
```json
{
  "Effect": "Allow",
  "Action": "fsx:CreateBackup",
  "Resource": "arn:aws:fsx:us-east-1:123456789012:file-system/*"
}
```

## Sample Policy: Backup Only Access
This policy allows a system or user to view FSx resources and take backups, but prevents them from deleting or modifying the file systems.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowFSxReadAndBackup",
      "Effect": "Allow",
      "Action": [
        "fsx:Describe*",
        "fsx:ListTagsForResource",
        "fsx:CreateBackup"
      ],
      "Resource": "*"
    }
  ]
}
```
