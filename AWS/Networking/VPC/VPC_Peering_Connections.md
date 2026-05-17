# VPC Peering Connections

## What are VPC Peering Connections?

A VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them using private IPv4 addresses or IPv6 addresses. 

When you peer two VPCs together, instances in either VPC can communicate with each other as if they were located within the exact same network. 

**Key Characteristics:**
* **Infrastructure:** It is not a gateway or a VPN connection, and it does not rely on a separate piece of physical hardware. AWS uses its existing internal infrastructure to route the traffic.
* **Performance:** Because it uses the AWS backbone, there is no single point of failure or bandwidth bottleneck.
* **One-to-One:** A peering connection is strictly a one-to-one relationship between two VPCs.
* **Scope:** You can peer VPCs within the same AWS Region, across different AWS Regions (Inter-Region VPC Peering), and even across different AWS Accounts.

## What is it used for?

VPC peering is primarily used to securely and privately link environments together. Common use cases include:

1. **Shared Services VPC:** 
   You might have multiple application VPCs (e.g., `App-A-VPC`, `App-B-VPC`) that all need access to centralized services like Active Directory, logging, monitoring, or CI/CD pipelines. You can put these shared tools in a `Shared-Services-VPC` and peer all application VPCs to it.
2. **Cross-Account Connectivity:** 
   If your organization uses a multi-account strategy, or if you need to integrate your network with a partner, vendor, or customer's AWS environment, you can peer a VPC in your account with a VPC in theirs.
3. **Inter-Region Disaster Recovery:** 
   By peering a VPC in `us-east-1` with a VPC in `eu-west-1`, you can privately replicate data (like databases or S3 buckets via endpoints) across regions for disaster recovery.
4. **Mergers and Acquisitions:** 
   When combining two companies' IT infrastructures, VPC peering allows the networks to communicate quickly without building complex VPNs (provided their IP ranges don't overlap).

### ⚠️ Crucial Limitations to Remember
* **No Transitive Peering:** If VPC `A` is peered with VPC `B`, and VPC `B` is peered with VPC `C`, **VPC `A` cannot talk to VPC `C`**. You would have to create a direct peering connection between `A` and `C`.
* **No Overlapping IP Ranges:** You cannot create a peering connection between two VPCs that have matching or overlapping IPv4 CIDR blocks.

---

## Step-by-Step Way to Set It Up

Setting up a peering connection involves a handshake process (Request -> Accept) followed by network configuration (Routing and Security).

### Step 1: Pre-Requisite Check
Before starting, look at the CIDR blocks of both VPCs. If VPC A is `10.0.0.0/16` and VPC B is `10.0.0.0/16` (or even `10.0.1.0/24`), peering will fail. They must be unique.

### Step 2: Request the Peering Connection
1. Log into the AWS Management Console and go to the **VPC Service**.
2. In the left navigation pane, select **Peering Connections**, then click **Create peering connection**.
3. **Name tag:** Give it a descriptive name (e.g., `Peer-AppA-to-SharedServices`).
4. **Requester:** Select the VPC in your current account that is initiating the request.
5. **Accepter:** Choose where the accepting VPC is located:
   * *My account* or *Another account* (requires the other Account ID).
   * *This Region* or *Another Region*.
6. Specify the Accepter VPC ID and click **Create peering connection**. The status will change to *Pending Acceptance*.

### Step 3: Accept the Peering Connection
*If the Accepter VPC is in another account or region, you must log into that account/region to do this step.*
1. Go to the **VPC Service** -> **Peering Connections**.
2. Select the pending peering connection.
3. Click the **Actions** dropdown and select **Accept Request**.
4. The status will change from *Pending Acceptance* to *Active*.
*(Note: The connection is now established, but traffic still won't flow until you configure the routes).*

### Step 4: Update Route Tables (The most forgotten step!)
Both VPCs need to know how to send traffic to each other over the new connection.

**In the Requester VPC:**
1. Go to Route Tables and select the route table(s) associated with your subnets.
2. Add a new route:
   * **Destination:** The CIDR block of the Accepter VPC (e.g., `172.31.0.0/16`).
   * **Target:** Select **Peering Connection**, and choose the ID (`pcx-0123456789abcdef0`).

**In the Accepter VPC:**
1. Go to Route Tables and select the route table(s) associated with its subnets.
2. Add a new route:
   * **Destination:** The CIDR block of the Requester VPC (e.g., `10.0.0.0/16`).
   * **Target:** Select the same Peering Connection ID (`pcx-0123456789abcdef0`).

### Step 5: Update Security Groups
Even though the networks are connected, instance-level firewalls still block traffic by default.
1. Go to the **Security Groups** of the instances that need to communicate.
2. Add an **Inbound Rule** to allow the required traffic (e.g., SSH, HTTP, or All Traffic).
3. Set the **Source** to the CIDR block of the peered VPC (or reference a specific Security Group ID from the peered VPC if they are in the same region).
