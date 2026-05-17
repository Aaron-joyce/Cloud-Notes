# Basic Networking in AWS using VPC

Amazon Virtual Private Cloud (Amazon VPC) is the foundational networking service in AWS. It allows you to provision a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.

## Core Components and Services

### 1. VPC (Virtual Private Cloud)
- **What it is:** A logically isolated virtual network defined by a primary IPv4 CIDR block (e.g., `10.0.0.0/16`).
- **Configuration:** You choose the IP address range for your VPC. It spans all the Availability Zones (AZs) within the selected AWS Region.

### 2. Subnets
- **What they are:** Sub-sections of the VPC's IP address range that are mapped to a specific Availability Zone. Subnets provide high availability and fault tolerance.
- **Types:**
  - **Public Subnet:** A subnet whose associated route table has a route to an Internet Gateway.
  - **Private Subnet:** A subnet whose associated route table does *not* have a route to an Internet Gateway.
- **Configuration:** Allocate a smaller CIDR block from the VPC's range (e.g., `10.0.1.0/24`). Assign the subnet to a specific AZ.

### 3. Internet Gateway (IGW)
- **What it is:** A highly available, horizontally scaled VPC component that allows communication between instances in your VPC and the internet.
- **Configuration:** Create the IGW and attach it to your VPC. It performs network address translation (NAT) for instances that have been assigned public IPv4 addresses.

### 4. Route Tables
- **What they are:** A set of rules, called routes, that are used to determine where network traffic from your subnet or gateway is directed.
- **Configuration:** 
  - Every VPC comes with a **Main Route Table**.
  - You can create **Custom Route Tables** and explicitly associate them with specific subnets.
  - Example Route (Public): Destination `0.0.0.0/0` -> Target `igw-id` (Routes internet-bound traffic to the IGW).

### 5. NAT Gateway
- **What it is:** A Network Address Translation (NAT) service. It allows instances in a private subnet to connect to services outside the VPC (like the internet or other AWS services) but prevents external services from initiating a connection with those instances.
- **Configuration:** 
  - Deploy the NAT Gateway in a **Public Subnet**.
  - Allocate an Elastic IP (EIP) address to the NAT Gateway.
  - Update the Private Subnet's route table to point internet-bound traffic (`0.0.0.0/0`) to the NAT Gateway.

### 6. Security Groups (SG)
- **What they are:** Stateful, instance-level firewalls that control inbound and outbound traffic. "Stateful" means if you send a request from your instance, the response traffic for that request is allowed to flow in regardless of inbound security group rules.
- **Configuration:** Attached directly to resources (e.g., EC2 instances, RDS databases). You define 'Allow' rules (deny by default) specifying the protocol, port range, and source/destination IP or another Security Group.

### 7. Network Access Control Lists (NACLs)
- **What they are:** Stateless, subnet-level firewalls. "Stateless" means you must explicitly define rules for both inbound and outbound traffic.
- **Configuration:** Associated with subnets. They act as a second layer of defense. You define ordered rules (e.g., Rule 100, Rule 200) that can either 'Allow' or 'Deny' traffic.

### 8. Elastic IP Addresses (EIP)
- **What they are:** Static public IPv4 addresses designed for dynamic cloud computing. 
- **Configuration:** Allocate an EIP to your account and associate it with an instance or a NAT Gateway. If an instance stops and starts, its standard public IP changes, but an EIP remains the same.

### 9. VPC Endpoints
- **What they are:** Enables private connections between your VPC and supported AWS services (like S3, DynamoDB) without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect.
- **Types:**
  - **Gateway Endpoints:** For Amazon S3 and DynamoDB. Uses route tables.
  - **Interface Endpoints (AWS PrivateLink):** Uses an Elastic Network Interface (ENI) with a private IP address in your subnet.

---

## How to Configure a Basic Architecture (Standard 3-Tier Flow)

A standard best-practice architecture involves deploying resources across multiple Availability Zones with both public and private subnets.

### Step-by-Step Configuration Flow:

1. **Create the VPC:**
   - Define a CIDR block (e.g., `10.0.0.0/16`).

2. **Create Subnets:**
   - Create Public Subnet 1 in AZ-a (`10.0.1.0/24`).
   - Create Public Subnet 2 in AZ-b (`10.0.2.0/24`).
   - Create Private Subnet 1 in AZ-a (`10.0.3.0/24`) - e.g., for App Servers.
   - Create Private Subnet 2 in AZ-b (`10.0.4.0/24`) - e.g., for Databases.

3. **Enable Internet Access:**
   - Create an **Internet Gateway (IGW)** and attach it to the VPC.
   - Create a **Public Route Table**. Add a route: `0.0.0.0/0` pointing to the `IGW`.
   - Associate the Public Route Table with *Public Subnet 1* and *Public Subnet 2*.

4. **Enable Outbound-Only Internet for Private Resources:**
   - Create a **NAT Gateway** in *Public Subnet 1* (requires an Elastic IP).
   - Create a **Private Route Table**. Add a route: `0.0.0.0/0` pointing to the `NAT Gateway`.
   - Associate the Private Route Table with *Private Subnet 1* and *Private Subnet 2*.

5. **Secure the Resources:**
   - Create a **Security Group for Web Servers (Public)**: Allow Inbound HTTP/HTTPS from `0.0.0.0/0`.
   - Create a **Security Group for App Servers (Private)**: Allow Inbound traffic only from the *Web Server Security Group*.
   - Create a **Security Group for Databases (Private)**: Allow Inbound traffic (e.g., Port 3306) only from the *App Server Security Group*.

This setup ensures that your web tier is accessible to the public, while your application logic and database remain completely isolated in private subnets, with secure, controlled outbound access for updates and API calls.
