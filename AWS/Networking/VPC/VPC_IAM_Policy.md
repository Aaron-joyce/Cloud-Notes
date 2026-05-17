# Amazon VPC IAM Policy Guide

VPC permissions govern the networking infrastructure, allowing users to create networks, modify route tables, and manage connectivity.

## Common Use Cases & Required Permissions

### 1. Network Read-Only
Allows an auditor or developer to view the network topology without making changes.
* **Required Actions**: `ec2:DescribeVpcs`, `ec2:DescribeSubnets`, `ec2:DescribeRouteTables`, `ec2:DescribeSecurityGroups`

*Sample Snippet (Viewing VPCs):*
```json
{
  "Effect": "Allow",
  "Action": "ec2:DescribeVpcs",
  "Resource": "*"
}
```

### 2. Network Administrator
Allows configuring the VPC, including creating subnets, route tables, peering connections, and internet gateways.
* **Required Actions**: `ec2:CreateVpc`, `ec2:CreateSubnet`, `ec2:CreateRouteTable`, `ec2:CreateRoute`, `ec2:CreateInternetGateway`

## Sample Policy: Restrict VPC Creation
This policy allows a user full access to manage EC2 resources (like instances), but explicitly prevents them from creating or deleting VPCs, Subnets, or Internet Gateways, ensuring they cannot modify the core network architecture.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEC2FullAccess",
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    },
    {
      "Sid": "DenyNetworkModifications",
      "Effect": "Deny",
      "Action": [
        "ec2:CreateVpc",
        "ec2:DeleteVpc",
        "ec2:CreateSubnet",
        "ec2:DeleteSubnet",
        "ec2:CreateInternetGateway",
        "ec2:DeleteInternetGateway",
        "ec2:CreateRouteTable",
        "ec2:DeleteRouteTable"
      ],
      "Resource": "*"
    }
  ]
}
```
