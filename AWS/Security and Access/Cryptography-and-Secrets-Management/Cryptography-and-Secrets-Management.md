# Cryptography & Secrets Management

Protecting data at rest and managing sensitive credentials securely are fundamental AWS best practices.

## 1. AWS Key Management Service (KMS)

AWS KMS makes it easy for you to create and manage cryptographic keys and control their use across a wide range of AWS services.

### Customer Master Keys (CMKs)
- **Symmetric CMKs**: The same key is used for encryption and decryption. This is the most common type of key in AWS.
- **Asymmetric CMKs**: Represents a mathematically related public key and private key pair. Used for encryption/decryption or signing/verification.

### Key Material Origins
- **AWS Managed Keys**: Created, managed, and used on your behalf by an AWS service (e.g., `aws/s3`). You cannot manage these directly.
- **Customer Managed Keys**: Keys that you create, own, and manage the lifecycle of, including rotation and policies.
- **Imported Key Material**: You can import your own key material from your on-premises key management infrastructure into a Customer Managed CMK.

### Envelope Encryption
AWS does not send your data to KMS to be encrypted. Instead, KMS generates a Data Encryption Key (DEK). The plain text data is encrypted using this DEK. Then, the DEK itself is encrypted under the root CMK. Both the encrypted data and the encrypted DEK are stored together.

### KMS Key Policies and Grants
- **Key Policies**: The primary way to control access to KMS keys. Unlike IAM, KMS keys *must* have a key policy attached to be usable.
- **Grants**: An alternative access control mechanism that allows you to programmatically delegate the use of KMS keys to other AWS principals (often used by AWS services).

## 2. Secrets & Certificate Handling

### AWS Secrets Manager
A service designed to securely store, retrieve, and manage database credentials, API keys, and other secrets throughout their lifecycle.
- Features native integration for automatically rotating database credentials (e.g., RDS) on a schedule using AWS Lambda.
- Supports cross-account access and fine-grained IAM policies.

### AWS Systems Manager Parameter Store
A capability of Systems Manager that provides hierarchical storage for configuration data management and secrets management.
- You can store data as plain text or encrypted strings (SecureStrings).
- While it stores secrets securely, it *lacks* the native, out-of-the-box scheduled auto-rotation features present in Secrets Manager.

### AWS Certificate Manager (ACM)
A service that lets you easily provision, manage, and deploy public and private Secure Sockets Layer/Transport Layer Security (SSL/TLS) certificates for use with AWS services (like Application Load Balancers or API Gateway).
- Provides automated provisioning, deployment, and renewal of certificates, eliminating manual certificate lifecycle management.
