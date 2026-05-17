# AWS CloudFormation

AWS CloudFormation is an Infrastructure as Code (IaC) engine that allows you to provision and update your AWS infrastructure deterministically.

## Configuration Management & Provisioning

### Deterministic Provisioning
CloudFormation allows you to define your entire infrastructure in JSON or YAML templates. This ensures that environments are created consistently, repeatedly, and predictably.

### Configuration Consistency
Because infrastructure is defined as code, it can be version-controlled, reviewed, and audited just like application code, ensuring configuration consistency across development, testing, and production environments.

### CloudFormation Hooks
A governance feature that allows you to evaluate resources before deployment. Hooks can execute custom logic (like validating that an S3 bucket is encrypted) and block the deployment if the resources do not comply with organizational standards.
