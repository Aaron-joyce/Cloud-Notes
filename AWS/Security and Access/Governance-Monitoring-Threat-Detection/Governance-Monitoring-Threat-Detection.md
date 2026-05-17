# Governance, Monitoring, & Threat Detection

Maintaining visibility into your AWS environment is critical for identifying misconfigurations and responding to active threats.

## 1. Continuous Audit & Logging

### AWS CloudTrail
A service that enables governance, compliance, and operational/risk auditing by recording API calls made within your AWS account.
- **Management Events**: Tracks operations performed on resources (e.g., `CreateBucket`, `RunInstances`). Enabled by default.
- **Data Events**: Tracks resource operations on or within a resource itself (e.g., `GetObject`, `PutObject` in S3, or DynamoDB `PutItem`). Must be explicitly enabled.
- **Multi-Region Trails & Log File Integrity Validation**: Ensures logs cover all regions and validates that log files have not been modified or deleted.

### AWS Config
A service that enables you to assess, audit, and evaluate the configurations of your AWS resources.
- **Configuration History**: Records historical configurations and changes to resources over time.
- **Compliance Rules**: Allows you to create rules (e.g., "All EBS volumes must be encrypted") and flags non-compliant resources.
- **Automated Remediation**: Can trigger AWS Systems Manager documents to automatically fix non-compliant resources.

### VPC Flow Logs
A feature that enables you to capture information about the IP traffic (metadata like source IP, destination IP, ports, bytes transferred, accept/reject status) flowing to and from network interfaces in your VPC. Useful for troubleshooting network connectivity and detecting malicious traffic patterns.

## 2. Managed Threat Intel & Security Management

### Amazon GuardDuty
A continuous security monitoring service that uses intelligent threat detection and machine learning to identify unexpected and potentially unauthorized or malicious activity.
- It analyzes multiple data sources: CloudTrail event logs, VPC Flow Logs, DNS Query Logs, EKS runtime activity, and S3 data events.
- It can detect issues like compromised EC2 instances communicating with known command-and-control servers, or unusual IAM API calls.

### AWS Security Hub
A centralized Cloud Security Posture Management (CSPM) service. It aggregates, organizes, and prioritizes security alerts (findings) from multiple AWS services (GuardDuty, Inspector, Macie, IAM Access Analyzer) and supported third-party solutions into a single dashboard.

### Amazon Macie
A fully managed data security and data privacy service. It uses machine learning and pattern matching to discover and protect sensitive data (such as Personally Identifiable Information [PII] or intellectual property) stored in Amazon S3 buckets.

### Amazon Inspector
An automated vulnerability management service that continually scans AWS workloads for software vulnerabilities and unintended network exposure. It scans Amazon EC2 instances, Amazon ECR container images, and AWS Lambda functions.
