# AWS Systems Manager - Session Manager Requirements

To successfully connect to an EC2 instance (both Linux and Windows) using AWS Systems Manager (SSM) Session Manager, several prerequisites must be met. Below are the key requirements necessary to enable Session Manager functionality.

## 1. SSM Agent Installed and Running
The **AWS Systems Manager Agent (SSM Agent)** must be installed and running on the EC2 instance.
*   **Linux**: The SSM Agent is pre-installed by default on several AMIs, including:
    *   Amazon Linux 2 and Amazon Linux 2023
    *   Ubuntu Server 16.04, 18.04, 20.04, and 22.04 LTS
    *   SUSE Linux Enterprise Server (SLES)
*   **Windows**: The SSM Agent is pre-installed on Windows Server AMIs provided by AWS (Windows Server 2016, 2019, 2022, etc.).
*   *Note: If you are using a custom AMI or an older OS, you may need to manually install or start the SSM Agent.*

## 2. IAM Instance Profile with Proper Permissions
The EC2 instance must have an IAM Role attached (an Instance Profile) that grants the SSM Agent permission to communicate with the Systems Manager service.
*   **Managed Policy**: The easiest way to grant these permissions is by attaching the AWS-managed policy `AmazonSSMManagedInstanceCore` to the IAM Role associated with the instance. This provides essential permissions for Session Manager, Patch Manager, and other SSM features.
*   **Custom Policy (Least Privilege)**: If you strictly want least privilege for *only* Session Manager (disabling Patch Manager, Run Command, etc.), you can attach a custom policy with only the following essential actions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:UpdateInstanceInformation",
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel",
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply"
            ],
            "Resource": "*"
        }
    ]
}
```
*Note: `ssm:UpdateInstanceInformation` allows the instance to register its health. The `ssmmessages:*` actions manage the actual session channels, and the `ec2messages:*` actions are required for the SSM Agent to receive core control instructions and health checks from the service.*

## 3. Network Connectivity to Systems Manager Endpoints
The instance must be able to securely communicate with the AWS Systems Manager endpoints. Since Session Manager does not require inbound ports (like SSH port 22 or RDP port 3389) to be open, it entirely relies on outbound connectivity initiated by the SSM Agent.
You can achieve this in one of the following ways:
*   **Public Subnet**: The instance has a public IP address and routes traffic through an Internet Gateway (IGW).
*   **Private Subnet with NAT Gateway**: The instance routes outbound internet traffic through a NAT Gateway.
*   **Private Subnet with VPC Endpoints**: For fully private networks without internet access, you must configure VPC Endpoints (AWS PrivateLink) for Systems Manager. At a minimum, you need endpoints for:
    *   `com.amazonaws.[region].ssm`
    *   `com.amazonaws.[region].ssmmessages`
    *   `com.amazonaws.[region].ec2messages`

## 4. Supported Operating System
Ensure the operating system version is supported by the SSM Agent. Most modern Linux and Windows versions are supported, but extremely outdated versions may not be.

## 5. Security Group Configuration
*   **Inbound Rules**: You **do not** need to open any inbound ports (e.g., port 22 for SSH or 3389 for RDP) for Session Manager to work. This is one of the primary security benefits of Session Manager.
*   **Outbound Rules**: The Security Group attached to the instance must allow outbound HTTPS (port 443) traffic so the SSM Agent can reach the AWS Systems Manager API endpoints.

## 6. KMS Key for Session Encryption (Optional but Recommended)
By default, Session Manager encrypts session data in transit using TLS. However, you can configure Session Manager to further encrypt the session data using an AWS Key Management Service (KMS) key. If you enable this:
*   The instance's IAM role must have permission to use the KMS key (`kms:Decrypt` and `kms:GenerateDataKey`).
*   The IAM user or role initiating the session must also have permission to use the KMS key.

## Summary Checklist
- [ ] SSM Agent is installed and the service is running (`amazon-ssm-agent`).
- [ ] IAM Role with `AmazonSSMManagedInstanceCore` is attached to the EC2 instance.
- [ ] Instance has outbound internet access (via IGW/NAT) OR VPC Endpoints for SSM are configured.
- [ ] Security Group allows outbound traffic on Port 443 (HTTPS).
