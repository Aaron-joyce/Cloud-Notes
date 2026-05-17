# Amazon EC2 IAM Policy Guide

When working with EC2, you need IAM permissions to launch, manage, and view instances and their associated resources (EBS volumes, Security Groups, ENIs).

## Common Use Cases & Required Permissions

### 1. Read-Only Access
Used by auditors or monitoring tools to view instances without modifying them.
* **Required Actions**: `ec2:Describe*`

### 2. EC2 Developer / Contributor
Used by developers who need to launch, stop, and terminate instances, as well as manage their security groups.
* **Required Actions**:
  * `ec2:Describe*` (View resources)
  * `ec2:RunInstances` (Launch new instances)
  * `ec2:TerminateInstances`, `ec2:StopInstances`, `ec2:StartInstances` (Lifecycle management)
  * `ec2:CreateTags` (Tagging instances on creation)
  * `ec2:AuthorizeSecurityGroupIngress`, `ec2:RevokeSecurityGroupIngress` (Managing firewall rules)

*Sample Snippet (RunInstances requires permission to attach a subnet and security group):*
```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:RunInstances"
  ],
  "Resource": [
    "arn:aws:ec2:*:*:instance/*",
    "arn:aws:ec2:*:*:subnet/*",
    "arn:aws:ec2:*:*:security-group/*",
    "arn:aws:ec2:*:*:image/*"
  ]
}
```

## Sample Policy: Least-Privilege EC2 Developer
This policy allows a developer to view all EC2 resources, but they can only start, stop, or terminate instances that have the tag `Environment: Development`.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ViewAllEC2Resources",
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    },
    {
      "Sid": "ManageDevInstancesOnly",
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Environment": "Development"
        }
      }
    }
  ]
}
```
