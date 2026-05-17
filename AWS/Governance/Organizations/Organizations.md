# AWS Organizations

AWS Organizations is the foundational service used to centrally manage and govern a multi-account AWS environment.

## Landing Zone & Multi-Account Architecture

### Centralized Management
Organizations allows you to consolidate multiple AWS accounts into an organization that you create and centrally manage. It provides consolidated billing, allowing you to track costs across all accounts.

### Organizational Units (OUs)
You can group accounts into logical structures called Organizational Units (OUs) based on business function, environment (e.g., Development, Production), or security requirements.

### Service Control Policies (SCPs)
SCPs act as top-level boundary guardrails to restrict API actions across account groups (OUs). 
- **Preventive Guardrails**: They do not grant permissions; they explicitly deny access. Even if an IAM user is granted `AdministratorAccess`, an SCP can prevent them from performing certain actions.
- **Common Use Cases**: Preventing regions from being used, denying the creation of unencrypted resources, or preventing the deletion of VPC Flow Logs.
