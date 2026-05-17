# AWS Config

AWS Config is a continuous monitoring and assessment service that maintains an inventory of your AWS resources and tracks their detailed configuration histories.

## Compliance Tracking & Resource Auditing

### Continuous Monitoring and Inventory
Config automatically tracks changes to your resource configurations, creating a timeline of how a resource (like an EC2 instance or S3 bucket) has been modified over time.

### Compliance Blueprints (AWS Config Rules)
It evaluates resource changes against predefined or custom compliance blueprints (Config Rules).
- **Managed Rules**: AWS provides hundreds of managed rules (e.g., `s3-bucket-ssl-requests-only`, `encrypted-volumes`).
- **Custom Rules**: You can build custom rules using AWS Lambda functions.

### Automated Remediation
When a resource is flagged as non-compliant, AWS Config can initiate automated remediation scripts via AWS Systems Manager Automation documents to automatically fix the issue (e.g., turning on encryption).
