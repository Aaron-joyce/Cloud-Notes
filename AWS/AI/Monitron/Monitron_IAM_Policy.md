# Amazon Monitron IAM Policy Guide

Monitron IAM policies control administrative access to the Monitron project and the setup of sensors/gateways.

## Common Use Cases & Required Permissions

### 1. Monitron Project Administrator
Allows creating a project, registering sensors, and managing user access within the Monitron app.
* **Required Actions**: `monitron:CreateProject`, `monitron:UpdateProject`, `monitron:GetProject`

*Sample Snippet (Viewing project details):*
```json
{
  "Effect": "Allow",
  "Action": "monitron:GetProject",
  "Resource": "arn:aws:monitron:us-east-1:123456789012:project/my-factory-project"
}
```

## Sample Policy: IAM Identity Center Integration
Because Monitron relies on AWS IAM Identity Center (SSO) for authenticating the technicians who use the mobile app, administrators often need permissions to configure this link.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowMonitronAdmin",
      "Effect": "Allow",
      "Action": "monitron:*",
      "Resource": "*"
    },
    {
      "Sid": "AllowSSOLink",
      "Effect": "Allow",
      "Action": [
        "sso:DescribeInstance",
        "sso:ListDirectoryAssociations"
      ],
      "Resource": "*"
    }
  ]
}
```
