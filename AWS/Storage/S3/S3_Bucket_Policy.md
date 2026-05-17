# Amazon S3 Bucket Policy Guide

Unlike Identity-Based Policies which are attached to users or roles, an S3 Bucket Policy is a Resource-Based Policy attached directly to the bucket itself. It dictates exactly who can access the bucket, regardless of their IAM identity policies.

## Common Use Cases & Required Configurations

### 1. Enforcing HTTPS (Encryption in Transit)
A best practice is to reject any requests made to the bucket that do not use HTTPS.
* **Condition**: Check that `aws:SecureTransport` is true.

### 2. Cross-Account Access
Allowing a user or role from a completely different AWS account to read objects in your bucket.
* **Principal**: Specify the AWS Account ID or Role ARN of the external account.

*Sample Snippet (Allowing external account read access):*
```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::999999999999:root"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-shared-bucket/*"
}
```

## Sample Policy: Enforce HTTPS & Require Specific IP
This bucket policy enforces that all traffic must be over HTTPS. It also explicitly denies any access to the bucket if the request does NOT originate from a specific corporate IP address range.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceHTTPS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-secure-bucket",
        "arn:aws:s3:::my-secure-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    },
    {
      "Sid": "DenyOutsideCorporateNetwork",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-secure-bucket",
        "arn:aws:s3:::my-secure-bucket/*"
      ],
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```
