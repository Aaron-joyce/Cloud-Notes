# Amazon CloudFront IAM Policy Guide

CloudFront IAM permissions control who can create distributions, invalidate caches, and manage edge functions.

## Common Use Cases & Required Permissions

### 1. Cache Administrator (Invalidations)
Allows a CI/CD pipeline or developer to clear the cache after deploying a new version of a website.
* **Required Actions**: `cloudfront:CreateInvalidation`, `cloudfront:GetInvalidation`

*Sample Snippet (Creating an invalidation):*
```json
{
  "Effect": "Allow",
  "Action": "cloudfront:CreateInvalidation",
  "Resource": "arn:aws:cloudfront::123456789012:distribution/EDFDVBD632BHDS5"
}
```

### 2. Distribution Manager
Allows configuring the CDN, adding origins, and changing cache behaviors.
* **Required Actions**: `cloudfront:UpdateDistribution`, `cloudfront:GetDistribution`

## Sample Policy: CI/CD Pipeline Cache Clearing
This policy allows an automated pipeline to clear the CloudFront cache for a specific distribution without granting permission to change the distribution's settings.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowInvalidations",
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation",
        "cloudfront:GetInvalidation",
        "cloudfront:ListInvalidations"
      ],
      "Resource": "arn:aws:cloudfront::123456789012:distribution/EDFDVBD632BHDS5"
    }
  ]
}
```
