# Amazon API Gateway IAM Policy Guide

IAM in API Gateway controls who can create and deploy APIs, as well as who can invoke them (if IAM Authorization is enabled).

## Common Use Cases & Required Permissions

### 1. API Developer
Allows creating, configuring, and deploying APIs.
* **Required Actions**: `apigateway:GET`, `apigateway:POST`, `apigateway:PUT`, `apigateway:PATCH`, `apigateway:DELETE`

*Sample Snippet (Deploying an API):*
```json
{
  "Effect": "Allow",
  "Action": "apigateway:POST",
  "Resource": "arn:aws:apigateway:us-east-1::/restapis/*/deployments"
}
```

### 2. API Invoker (IAM Authorization)
Allows a client to actually call an API endpoint when the method is protected by `AWS_IAM` authorization.
* **Required Actions**: `execute-api:Invoke`

## Sample Policy: API Invoker
This policy allows a specific IAM user or role to call the `GET /users` method on a specific API Gateway deployment.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowInvokeAPI",
      "Effect": "Allow",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:us-east-1:123456789012:a1b2c3d4e5/prod/GET/users"
    }
  ]
}
```
