# Amazon ECS IAM Policy Guide

When working with Amazon ECS, IAM permissions are divided into two main categories: user permissions (to manage the cluster) and task permissions (what the containers are allowed to do).

## Common Use Cases & Required Permissions

### 1. Read-Only Access
To view clusters, services, and running tasks.
* **Required Actions**: `ecs:List*`, `ecs:Describe*`

### 2. ECS Application Developer
Needs to deploy new revisions of task definitions and update services.
* **Required Actions**:
  * `ecs:RegisterTaskDefinition` (Create new task versions)
  * `ecs:UpdateService` (Deploy the new version)
  * `iam:PassRole` (CRITICAL: Required to pass the Task Execution Role and Task Role to the ECS service)

*Sample Snippet (iam:PassRole is required to deploy tasks):*
```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": [
    "arn:aws:iam::*:role/ecsTaskExecutionRole",
    "arn:aws:iam::*:role/myApplicationTaskRole"
  ]
}
```

## Sample Policy: ECS Service Updater
This policy allows a developer to view ECS resources, register new task definitions, and update a specific service to trigger deployments. It restricts the roles they can pass to ensure they can't escalate privileges.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowViewECS",
      "Effect": "Allow",
      "Action": [
        "ecs:Describe*",
        "ecs:List*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowTaskRegistration",
      "Effect": "Allow",
      "Action": "ecs:RegisterTaskDefinition",
      "Resource": "*"
    },
    {
      "Sid": "AllowServiceUpdate",
      "Effect": "Allow",
      "Action": "ecs:UpdateService",
      "Resource": "arn:aws:ecs:*:*:service/my-cluster/my-web-service"
    },
    {
      "Sid": "AllowPassRoleToECS",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "ecs-tasks.amazonaws.com"
        }
      }
    }
  ]
}
```
