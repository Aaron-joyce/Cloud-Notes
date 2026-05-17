# AWS Service Catalog

AWS Service Catalog is a platform that allows central IT administrators to create, govern, and manage catalogs of approved AWS resources and CloudFormation stacks.

## Configuration Management & Provisioning

### Centralized Governance
It ensures that self-service builders (like developers or data scientists) can deploy infrastructure while strictly staying within organizational cost, compliance, and tagging constraints.

### Approved Portfolios
Administrators create "Portfolios" of approved "Products" (which are underlying CloudFormation templates). 

### Self-Service Empowerment
End-users can browse the catalog and launch these approved products without needing deep AWS knowledge or administrative IAM permissions, as Service Catalog assumes a pre-configured IAM role to provision the resources on their behalf.
