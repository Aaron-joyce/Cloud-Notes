# AWS Systems Manager

AWS Systems Manager (SSM) is an operational control hub used to manage hybrid infrastructure resources, including EC2 instances, on-premises servers, and edge devices.

## Configuration Management & Provisioning

### Patch Manager
Enforces automated OS update baselines. It allows you to define rules for auto-approving patches and schedules maintenance windows to roll them out across your fleet, ensuring compliance with security standards.

### State Manager
A configuration management service that prevents configuration drift on servers. It ensures that your instances remain in a consistent, defined state (e.g., ensuring specific antivirus software is installed and running).

### Parameter Store
Provides centralized, hierarchical configuration data management. It allows you to store parameters (like database connection strings) and secrets as plain text or encrypted data, separating configuration from your application code.
