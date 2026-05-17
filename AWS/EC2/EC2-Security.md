# AWS EC2 Security

Securing Amazon EC2 instances involves a multi-layered approach that spans identity and access management, network security, operating system security, and data encryption. Under the AWS Shared Responsibility Model, AWS is responsible for the security *of* the cloud (infrastructure, hardware, networking), while the customer is responsible for security *in* the cloud (OS patching, data encryption, network traffic routing, access control).

Here is an in-depth breakdown of the services, features, and concepts used to secure EC2 instances.

---

## 1. Security Groups (Virtual Firewalls)
Security Groups act as a stateful, virtual firewall for your EC2 instances to control inbound and outbound traffic.

* **Stateful Nature**: If you send a request from your instance (outbound), the response traffic for that request is automatically allowed to flow back in, regardless of inbound security group rules.
* **Instance-Level Protection**: Security groups are applied directly to the Elastic Network Interface (ENI) of an EC2 instance, not to the subnet.
* **Allow-Only Rules**: By default, security groups block all inbound traffic and allow all outbound traffic. You can only create *allow* rules; you cannot create *deny* rules.
* **Referencing**: You can reference other security groups in a rule (e.g., allowing traffic to your Database security group only from instances associated with your Web Server security group).

## 2. Key Pairs (Authentication)
Amazon EC2 uses public-key cryptography to encrypt and decrypt login information. 

* **Public/Private Keys**: AWS stores the public key on the EC2 instance, and you store the private key locally.
* **SSH and RDP**: You use the private key to securely SSH into Linux instances or retrieve the Administrator password for RDP access to Windows instances.
* **Security Best Practice**: Never share private keys. It is recommended to use modern alternatives like Session Manager or EC2 Instance Connect to avoid managing long-lived SSH keys entirely.

## 3. IAM Roles for EC2 (Instance Profiles)
Instead of storing long-term AWS credentials (Access Keys and Secret Access Keys) directly on an EC2 instance or in code to access other AWS services (like S3 or DynamoDB), you should use IAM Roles.

* **Instance Profiles**: An instance profile is a container for an IAM role that you can use to pass role information to an EC2 instance when the instance starts.
* **Temporary Credentials**: The EC2 instance automatically retrieves temporary, rotating security credentials via the Instance Metadata Service (IMDS).
* **Principle of Least Privilege**: Roles ensure that an instance only has exactly the permissions it needs to perform its specific tasks.

## 4. Modern Access Methods (Replacing SSH/RDP)
Managing and rotating SSH keys or opening inbound ports (22/3389) can be security risks. AWS provides secure alternatives:

### AWS Systems Manager (SSM) Session Manager
Session Manager provides secure and auditable instance management without the need to open inbound ports, maintain bastion hosts, or manage SSH keys.
* **No Open Ports**: It communicates via an outbound connection to the Systems Manager service endpoint. You can keep port 22 (SSH) and 3389 (RDP) completely closed in your Security Groups.
* **Auditing and Logging**: All session activity (commands executed) can be logged to Amazon CloudWatch Logs or Amazon S3 for compliance.

### EC2 Instance Connect (EIC)
EC2 Instance Connect provides a simple and secure way to connect to your Linux instances using Secure Shell (SSH).
* **Short-Lived Keys**: When you connect, the EIC API pushes a one-time-use SSH public key to the instance metadata where it remains for just 60 seconds. 
* **IAM Integration**: Access is governed by IAM policies, meaning you don't need to distribute permanent SSH keys to developers. You can revoke access centrally in IAM.

## 5. Amazon Inspector (Vulnerability Management)
Amazon Inspector is an automated vulnerability management service that continually scans AWS workloads for software vulnerabilities and unintended network exposure.

* **Continuous Scanning**: It automatically discovers running EC2 instances and scans them for Common Vulnerabilities and Exposures (CVEs).
* **Contextual Risk Routing**: Inspector assesses the vulnerability and its environment (e.g., is the instance publicly reachable?) to calculate a highly contextual risk score.
* **SSM Agent Dependency**: Inspector relies on the AWS Systems Manager (SSM) Agent installed on the EC2 instances to perform deep host-level vulnerability assessments.

## 6. AWS Nitro System
The AWS Nitro System is the underlying architecture for modern EC2 instances, providing enhanced security at the hardware level.

* **Hardware Offloading**: Nitro offloads virtualization, networking, and security functions to purpose-built hardware and software, minimizing the hypervisor attack surface and giving instances near bare-metal performance.
* **Nitro Enclaves**: Allows you to create highly isolated compute environments (enclaves) attached to EC2 instances. They have no persistent storage, no interactive access, and no external networking, making them perfect for processing highly sensitive data (PII, cryptographic keys).

## 7. Data Encryption

### Encryption at Rest (EBS Encryption)
Amazon Elastic Block Store (EBS) encryption offers seamless encryption of EBS data volumes, boot volumes, and snapshots using AWS Key Management Service (KMS).
* **Transparent to Applications**: The encryption occurs on the underlying servers that host EC2 instances, encrypting data as it moves between the EC2 instance and the EBS volume.
* **Default Encryption**: You can configure your AWS account to enforce encryption on all newly created EBS volumes by default, ensuring compliance.

### Encryption in Transit
* Network traffic between EC2 instances in the same VPC can be encrypted. 
* AWS Nitro-based instances automatically encrypt traffic in transit between instances within a VPC or peered VPCs at the hardware level.

## 8. Network Access Control Lists (NACLs)
While Security Groups operate at the instance level, NACLs act as a firewall for associated **Subnets**, controlling both inbound and outbound traffic at the subnet boundary.
* **Stateless**: Responses to allowed inbound traffic are subject to the rules for outbound traffic (and vice versa). You must explicitly open ephemeral ports for return traffic.
* **Allow and Deny Rules**: Unlike Security Groups, NACLs support explicit *deny* rules. They are typically used as an additional layer of defense to block specific malicious IP addresses from entering the subnet entirely.

## 9. Instance Metadata Service v2 (IMDSv2)
The Instance Metadata Service provides data about your instance that can be used to configure or manage the running instance.
* **Protection against SSRF**: IMDSv2 adds protection against Server-Side Request Forgery (SSRF) vulnerabilities by requiring session tokens for metadata retrieval, whereas IMDSv1 relied entirely on a simple HTTP GET request.
* **Enforcement**: It is a security best practice to enforce the use of IMDSv2 and disable IMDSv1 on all EC2 instances.
