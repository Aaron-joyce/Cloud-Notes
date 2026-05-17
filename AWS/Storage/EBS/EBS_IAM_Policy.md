# Amazon EBS IAM Policy Guide

EBS permissions are often intertwined with EC2 permissions, but you can explicitly control who can manage volumes and snapshots.

## Common Use Cases & Required Permissions

### 1. Snapshot Backup Administrator
Responsible for creating and managing backups (snapshots) of EBS volumes.
* **Required Actions**: `ec2:CreateSnapshot`, `ec2:DeleteSnapshot`, `ec2:DescribeSnapshots`

*Sample Snippet (Allowing snapshot creation):*
```json
{
  "Effect": "Allow",
  "Action": "ec2:CreateSnapshot",
  "Resource": "arn:aws:ec2:*:*:volume/*"
}
```

## Sample Policy: Volume Manager
This policy allows a user to create, attach, detach, and delete EBS volumes.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ManageVolumes",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateVolume",
        "ec2:DeleteVolume",
        "ec2:AttachVolume",
        "ec2:DetachVolume",
        "ec2:DescribeVolumes"
      ],
      "Resource": "*"
    }
  ]
}
```
