# AWS Control Tower

AWS Control Tower is an orchestration service that automates the setup of a secure, multi-account AWS environment based on AWS best practices.

## Landing Zone & Multi-Account Architecture

### Automated Landing Zone
Control Tower provides the easiest way to set up and govern a secure, multi-account AWS environment (a "Landing Zone"). It abstracts away the complexity of configuring underlying services manually.

### Orchestration of AWS Services
It automatically configures:
- AWS Organizations for account management.
- AWS Single Sign-On (IAM Identity Center) for access management.
- AWS CloudTrail and AWS Config for central logging and auditing.

### Pre-packaged Guardrails
Control Tower applies mandatory and elective guardrails to your OUs.
- **Preventive Guardrails**: Implemented via AWS Organizations Service Control Policies (SCPs) to stop non-compliant actions.
- **Detective Guardrails**: Implemented via AWS Config rules to detect and alert on non-compliant resources.
