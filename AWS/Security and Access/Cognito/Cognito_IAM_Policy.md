# Amazon Cognito IAM Policy Guide

Cognito requires two distinct sets of IAM permissions: identity management (who can configure Cognito) and user access (what resources an authenticated user can touch via Identity Pools).

## Common Use Cases & Required Permissions

### 1. Application Backend (User Management)
Allows a backend server (like a Lambda function) to programmatically create users, force password resets, or delete accounts.
* **Required Actions**: `cognito-idp:AdminCreateUser`, `cognito-idp:AdminDeleteUser`, `cognito-idp:AdminSetUserPassword`

*Sample Snippet (Admin creating a user):*
```json
{
  "Effect": "Allow",
  "Action": "cognito-idp:AdminCreateUser",
  "Resource": "arn:aws:cognito-idp:us-east-1:123456789012:userpool/us-east-1_xxxxxxxxx"
}
```

## Sample Policy: Authenticated User (Identity Pool)
This policy is NOT attached to an administrator. Instead, it is attached to the IAM Role assumed by an **Identity Pool** after a user successfully logs in. It grants the end-user direct, limited access to specific AWS resources, like uploading a profile picture to a specific folder in S3.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowUserToUploadProfilePic",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-user-uploads/${cognito-identity.amazonaws.com:sub}/*"
      ]
    }
  ]
}
```
*Note: The `${cognito-identity.amazonaws.com:sub}` variable dynamically restricts the user to only read/write files inside a folder named after their unique Cognito ID.*
