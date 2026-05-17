# AWS Transit Gateway

As your AWS infrastructure grows from a few VPCs to hundreds of VPCs, managing point-to-point connections becomes a massive operational burden. AWS Transit Gateway (TGW) solves this by acting as a central, highly scalable cloud router.

---

## 1. What are the core components?

### Transit Gateway
A Transit Gateway is a network transit hub that allows you to interconnect your Virtual Private Clouds (VPCs) and your on-premises networks. Instead of building a complex web of individual connections between every single network, you connect everything to the central Transit Gateway in a **Hub-and-Spoke** topology.

### Transit Gateway Attachments
An attachment is the actual link between the Transit Gateway and a network resource. You can attach multiple types of resources to a TGW:
*   **VPC Attachments:** Connecting an AWS VPC.
*   **VPN Attachments:** Connecting an on-premises network via a Site-to-Site IPSec VPN.
*   **Direct Connect Gateway Attachments:** Connecting an on-premises network via a dedicated AWS Direct Connect fiber link.
*   **Peering Attachments:** Connecting a Transit Gateway in one AWS Region to a Transit Gateway in another AWS Region.

### Transit Gateway Route Tables
Just like a VPC has route tables, a Transit Gateway has its own route tables to dictate how traffic flows *between* its attachments.
*   By default, a TGW has a single Default Route Table. If all attachments share this table, all connected networks can communicate with each other.
*   **Network Isolation:** You can create multiple custom TGW Route Tables. For example, you can attach your "Dev VPCs" to a "Dev Route Table" and "Prod VPCs" to a "Prod Route Table". This allows them to use the same central TGW infrastructure while remaining completely isolated from each other.

---

## 2. Transit Gateway vs. VPC Peering

While both connect networks, they are used for entirely different scales.

| Feature | VPC Peering | Transit Gateway (TGW) |
| :--- | :--- | :--- |
| **Topology** | Point-to-Point (Full Mesh required for many VPCs) | Hub-and-Spoke |
| **Transitivity** | **No.** (If A peers to B, and B peers to C, A cannot talk to C). | **Yes.** (Traffic routes fluidly between all attachments based on route tables). |
| **Management at Scale** | Extremely complex. Connecting 100 VPCs requires 4,950 peering connections `(n(n-1)/2)`. | Simple. Connecting 100 VPCs requires 100 attachments to the central TGW. |
| **On-Premises Integration** | Cannot do "Edge-to-Edge" routing. A VPN connected to VPC A cannot be used to reach peered VPC B. | Native integration. A VPN attached to the TGW can route to all attached VPCs. |
| **Cost** | You only pay for Data Transfer. The connection itself is free. | You pay an hourly rate per attachment + a per-GB data processing fee. |
| **Best For** | Connecting 2 to 5 VPCs where cost is a primary concern. | Enterprise architectures with many VPCs, hybrid cloud environments, and centralized inspection. |

---

## 3. Detailed Step-by-Step Setup

**Scenario:** We want to connect `VPC-A` (10.1.0.0/16) to `VPC-B` (10.2.0.0/16) using a central Transit Gateway.

### Step 1: Create the Transit Gateway
1. Go to the **VPC Console**.
2. On the left navigation pane, scroll down to **Transit gateways** and click **Create transit gateway**.
3. **Name tag:** Give it a name (e.g., `Central-Corp-TGW`).
4. **ASN (Autonomous System Number):** You can leave the default Amazon ASN (64512) unless you are integrating with an on-premises BGP network that requires a specific custom ASN.
5. **Default Settings:** Leave *Default route table association* and *Default route table propagation* **enabled**. This makes the initial setup much easier by auto-populating routes.
6. Click **Create transit gateway** and wait for its state to become *Available*.

### Step 2: Create the Transit Gateway Attachments
You must tell the TGW which networks to plug into.
1. In the left pane, click **Transit gateway attachments**, then **Create transit gateway attachment**.
2. **Name tag:** `Attachment-VPC-A`
3. **Transit gateway ID:** Select the `Central-Corp-TGW` you just created.
4. **Attachment type:** Choose **VPC**.
5. **VPC ID:** Select `VPC-A`.
6. **Subnet IDs:** Select at least one subnet in every Availability Zone where you have resources that need to use the TGW. *(AWS drops a hidden Elastic Network Interface (ENI) into these subnets to handle the traffic).*
7. Click **Create transit gateway attachment**.
8. **REPEAT this entire process** to create a second attachment for `VPC-B`.

### Step 3: Verify the TGW Route Table
Because we left "Default propagation" enabled in Step 1, the TGW automatically learns the CIDR blocks of the VPCs as soon as the attachments are active.
1. Go to **Transit gateway route tables**.
2. Select the default route table.
3. Click the **Routes** tab.
4. You should automatically see:
   *   Destination: `10.1.0.0/16` -> Target: `Attachment-VPC-A`
   *   Destination: `10.2.0.0/16` -> Target: `Attachment-VPC-B`

### Step 4: Update the VPC Route Tables (The most common point of failure)
The TGW knows how to reach the VPCs, but the EC2 instances inside those VPCs don't know the TGW exists. You must update your standard VPC Route Tables.

**In VPC-A:**
1. Go to standard **Route Tables** in the VPC console and select the route table used by VPC-A's subnets.
2. Click **Edit routes** -> **Add route**.
3. **Destination:** Enter the CIDR block of VPC-B (`10.2.0.0/16`). *(Or enter `10.0.0.0/8` if you want all corporate traffic to go to the TGW).*
4. **Target:** Select **Transit Gateway**, and choose your `Central-Corp-TGW` ID.
5. Save changes.

**In VPC-B:**
1. Select the route table used by VPC-B's subnets.
2. Click **Edit routes** -> **Add route**.
3. **Destination:** Enter the CIDR block of VPC-A (`10.1.0.0/16`).
4. **Target:** Select the same Transit Gateway ID.
5. Save changes.

### Step 5: Update Security Groups
Traffic is now routing successfully, but instance-level firewalls might still block it.
1. Go to the **Security Groups** attached to the instances in VPC-A.
2. Add an Inbound rule allowing the required traffic (e.g., All ICMP for ping, or TCP 443) from VPC-B's CIDR (`10.2.0.0/16`).
3. Repeat for the instances in VPC-B, allowing inbound from VPC-A's CIDR.
