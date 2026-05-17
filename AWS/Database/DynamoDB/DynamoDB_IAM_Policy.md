# Amazon DynamoDB IAM Policy Guide

When working with DynamoDB, IAM controls who can read, write, and manage tables.

## Common Use Cases & Required Permissions

### 1. Application Read/Write Access
Used by applications (like a Lambda function or EC2 instance) to query or update data in a specific table.
* **Required Actions**: `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Scan`, `dynamodb:Query`, `dynamodb:UpdateItem`

*Sample Snippet (Granting read/write to a specific table):*
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:PutItem",
    "dynamodb:GetItem"
  ],
  "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/MyApplicationTable"
}
```

### 2. Database Administrator
Needs to create, delete, and manage table settings (like capacity or backups).
* **Required Actions**: `dynamodb:CreateTable`, `dynamodb:DeleteTable`, `dynamodb:UpdateTable`

## Sample Policy: Application Read/Write
This policy grants an application permission to read and write items, but restricts it to a specific table and its indexes.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAppReadWrite",
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Scan",
        "dynamodb:Query",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:123456789012:table/MyApplicationTable",
        "arn:aws:dynamodb:us-east-1:123456789012:table/MyApplicationTable/index/*"
      ]
    }
  ]
}
```
