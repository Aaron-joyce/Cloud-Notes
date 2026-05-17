# AWS Lambda IAM Policy Guide

When working with AWS Lambda, IAM is used for two main purposes: granting developers permission to deploy/manage the function, and granting the function itself permission to interact with other AWS services (the Execution Role).

## Common Use Cases & Required Permissions

### 1. Lambda Developer (Deployment Access)
Allows a developer to update the code and configuration of a function.
* **Required Actions**: 
  * `lambda:UpdateFunctionCode`, `lambda:UpdateFunctionConfiguration`
  * `iam:PassRole` (Required if the developer needs to change the function's execution role)

*Sample Snippet (Updating code):*
```json
{
  "Effect": "Allow",
  "Action": [
    "lambda:UpdateFunctionCode",
    "lambda:GetFunction"
  ],
  "Resource": "arn:aws:lambda:*:*:function:my-function"
}
```

### 2. Lambda Execution Role (What the function can do)
This policy is attached to the role assumed by the Lambda function, not the developer.
* **Required Actions**: At minimum, `logs:CreateLogStream` and `logs:PutLogEvents` to write logs to CloudWatch.

## Sample Policy: Lambda Developer with Least Privilege
This policy allows a developer to update the code and environment variables of a specific Lambda function, and invoke it for testing, but they cannot delete the function or change its execution role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListFunctions",
      "Effect": "Allow",
      "Action": "lambda:ListFunctions",
      "Resource": "*"
    },
    {
      "Sid": "AllowUpdateSpecificFunction",
      "Effect": "Allow",
      "Action": [
        "lambda:GetFunction",
        "lambda:GetFunctionConfiguration",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:InvokeFunction"
      ],
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:my-backend-service"
    }
  ]
}
```
