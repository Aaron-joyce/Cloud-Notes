# Network & Infrastructure Security

Securing the perimeter and internal traffic of your Virtual Private Cloud (VPC) is foundational to AWS security.

## 1. VPC Firewall Infrastructure

### Security Groups
Stateful, instance-level virtual firewalls.
- They evaluate traffic entering and leaving an Elastic Network Interface (ENI).
- **Stateful**: If you allow an inbound request, the outbound response is automatically allowed, regardless of outbound rules.
- You can only specify **Allow** rules (everything else is implicitly denied).

### Network Access Control Lists (NACLs)
Stateless, subnet-level virtual firewalls.
- They evaluate traffic entering and leaving a specific Subnet.
- **Stateless**: You must explicitly allow both inbound and outbound traffic.
- They use ordered rules (evaluated from lowest to highest number) and support both **Allow** and **Deny** rules.

### AWS Network Firewall
A managed service that makes it easy to deploy essential network protections for all your VPCs. It provides VPC-wide Layer 3 to Layer 7 inspection and stateful packet filtering, complete with an Intrusion Prevention System (IPS).

### AWS Route 53 Resolver DNS Firewall
Allows you to filter outbound DNS queries originating from your VPCs. You can block requests made to known malicious domains or sinkhole specific hostnames to prevent data exfiltration.

## 2. Perimeter and Connection Isolation

### Public vs. Private Subnet Topology Architecture
- **Public Subnet**: Contains resources that must be directly accessible from the internet (e.g., ALBs, NAT Gateways). A subnet is "public" if its route table directs internet-bound traffic to an Internet Gateway (IGW).
- **Private Subnet**: Contains resources that should not be directly addressable from the internet (e.g., EC2 application servers, RDS databases).

### NAT Gateways vs. NAT Instances
Resources in private subnets need a way to reach the internet (e.g., to download patches). 
- **NAT Gateway**: A highly available, AWS-managed service placed in the public subnet that translates private IPs to a public IP for outbound internet access.
- **NAT Instance**: A self-managed EC2 instance configured to perform network address translation.

### VPC Endpoints
Allows you to privately connect your VPC to supported AWS services without requiring an IGW, NAT device, or public IP addresses.
- **Gateway Endpoints**: Used exclusively for Amazon S3 and Amazon DynamoDB. They act as a target in your route table.
- **Interface Endpoints (AWS PrivateLink)**: Elastic Network Interfaces (ENIs) deployed directly into your subnets that act as the entry point for traffic destined to services like EC2 APIs, KMS, or SNS.

### AWS Systems Manager Session Manager
A fully managed service that lets you manage your EC2 instances through an interactive one-click browser-based shell or AWS CLI. It eliminates the need to open inbound SSH (port 22) or RDP (port 3389) ports via `0.0.0.0/0` in your Security Groups, vastly improving security.
