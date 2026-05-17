# Amazon S3 IAM Policy Guide

For S3, access is typically evaluated by checking both the Identity-Based Policy (attached to the user/role) AND the Resource-Based Policy (the Bucket Policy).

## Common Use Cases & Required Permissions

### 1. Application Read/Write Access
Used by applications that need to upload and download files from a specific bucket.
* **Required Actions**: `s3:GetObject`, `s3:PutObject`, `s3:ListBucket`

*Sample Snippet (Granting read/write to objects):*
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::my-application-bucket/*"
}
```

### 2. S3 Administrator
Manages bucket configurations (lifecycle, versioning, encryption) but doesn't necessarily need to read the data inside the objects.
* **Required Actions**: `s3:CreateBucket`, `s3:PutBucket*`, `s3:GetBucket*`

## Sample Policy: Application Bucket Access
This identity-based IAM policy allows an application to list the contents of a specific bucket and read/write objects within it. Note the difference in resources: `ListBucket` applies to the bucket itself, while `GetObject`/`PutObject` applies to the objects `/*` within the bucket.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-application-bucket"
    },
    {
      "Sid": "AllowReadWriteObjects",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-application-bucket/*"
    }
  ]
}
```
