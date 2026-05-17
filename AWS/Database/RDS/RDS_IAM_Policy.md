# Amazon RDS IAM Policy Guide

IAM for RDS primarily controls the management of the database instances. Data access (querying tables) is usually handled by the database's native authentication (unless using IAM Database Authentication).

## Common Use Cases & Required Permissions

### 1. Database Provisioner
Allows a developer to spin up and tear down test databases.
* **Required Actions**: `rds:CreateDBInstance`, `rds:DeleteDBInstance`, `rds:ModifyDBInstance`

*Sample Snippet (Stopping/Starting instances to save cost):*
```json
{
  "Effect": "Allow",
  "Action": [
    "rds:StartDBInstance",
    "rds:StopDBInstance"
  ],
  "Resource": "arn:aws:rds:us-east-1:123456789012:db:test-db-*"
}
```

### 2. IAM Database Authentication (Application Access)
Allows an application (like an EC2 instance) to connect to the database using its IAM role instead of a password.
* **Required Actions**: `rds-db:connect`

## Sample Policy: Application Connect via IAM Auth
This policy allows an application to authenticate to a specific database user (`db_user`) on a specific cluster using IAM.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRDSConnect",
      "Effect": "Allow",
      "Action": "rds-db:connect",
      "Resource": "arn:aws:rds-db:us-east-1:123456789012:dbuser:cluster-ABCDEFGHIJKL/db_user"
    }
  ]
}
```
