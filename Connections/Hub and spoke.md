# AWS Multi-VPC Interconnected Setup (Siloed Hub-and-Spoke)

This guide outlines the step-by-step process for creating a siloed yet interconnected multi-VPC environment using **AWS Transit Gateway (TGW)**. This architecture allows specific VPCs to access shared services while remaining isolated from one another.

---

## 1. Network Architecture Overview
* **VPC-A (Production):** Isolated workload.
* **VPC-B (Development):** Isolated workload.
* **VPC-Shared (Services):** Contains shared resources (e.g., Active Directory, NAT Gateways, Logging).
* **Connectivity Logic:** * VPC-A ↔ VPC-Shared (Allowed)
    * VPC-B ↔ VPC-Shared (Allowed)
    * VPC-A ↔ VPC-B (Blocked/Siloed)

---

## 2. Phase 1: Preparation & VPC Setup
Before creating the Gateway, ensure the foundational networking is correct.

### Step 1: CIDR Planning
Ensure no IP address overlap. Example:
* **VPC-A:** `10.1.0.0/16`
* **VPC-B:** `10.2.0.0/16`
* **VPC-Shared:** `10.10.0.0/16`

### Step 2: TGW Subnets
In each VPC, create a small, dedicated subnet (e.g., `/28`) in each Availability Zone (AZ) specifically for the Transit Gateway ENIs.
> **Note:** Do not place EC2 instances in these subnets; keep them reserved for the TGW attachments to simplify Network ACL management.

---

## 3. Phase 2: Create the Transit Gateway (TGW)
1.  Navigate to **VPC Dashboard > Transit Gateways > Create Transit Gateway**.
2.  **Name Tag:** `Global-Hub-TGW`.
3.  **Amazon Side ASN:** Use a private ASN (e.g., `64512`).
4.  **Crucial Settings (Disable Defaults):**
    * **Uncheck** `Default route table association`.
    * **Uncheck** `Default route table propagation`.
    * *Why?* Leaving these checked will automatically connect every VPC to every other VPC, breaking the "silo" requirement.
5.  Click **Create Transit Gateway**.

---

## 4. Phase 3: Create VPC Attachments
Connect each VPC to the TGW "Hub."

1.  Go to **Transit Gateway Attachments > Create Transit Gateway Attachment**.
2.  **Transit Gateway ID:** Select your `Global-Hub-TGW`.
3.  **Attachment Type:** VPC.
4.  **VPC ID:** Select VPC-A.
5.  **Subnets:** Select the dedicated TGW subnets created in Phase 1.
6.  **Repeat** steps 1-5 for **VPC-B** and **VPC-Shared**.

---

## 5. Phase 4: Configure Routing Logic (The "Silo")
You must manually create and configure two TGW Route Tables to define the traffic flow.

### TGW Route Table 1: "Isolate-Spokes"
* **Association:** Associate **VPC-A** and **VPC-B** attachments here.
* **Propagation:** Propagate **ONLY** the **VPC-Shared** attachment.
    * *Result:* VPC-A and VPC-B learn how to get to Shared, but they never learn about each other.

### TGW Route Table 2: "Shared-Services"
* **Association:** Associate the **VPC-Shared** attachment here.
* **Propagation:** Propagate **VPC-A**, **VPC-B**, and **VPC-Shared** attachments.
    * *Result:* The Shared VPC knows the routes to all spokes so it can respond to requests.

---

## 6. Phase 5: Update VPC Subnet Route Tables
The TGW is now configured, but individual subnets within your VPCs need to know to send traffic to the TGW.

1.  Go to **VPC > Route Tables**.
2.  **In VPC-A & VPC-B:** Add a route for `10.10.0.0/16` (VPC-Shared) with the target as the **Transit Gateway ID**.
3.  **In VPC-Shared:** Add routes for `10.1.0.0/16` (VPC-A) and `10.2.0.0/16` (VPC-B) with the target as the **Transit Gateway ID**.

---

## 7. Critical Considerations
* **Security Groups:** Security Groups are local. You must allow traffic from the *CIDR range* of the other VPC (e.g., VPC-Shared SG allows `10.1.0.0/16`).
* **NACLs:** Ensure Network ACLs on the TGW subnets are not blocking cross-VPC traffic.
* **Cost:** Remember TGW charges per hour per attachment plus a data processing fee ($0.02/GB).

---

## 8. Debugging Procedure
If connectivity fails, follow this hierarchy:

1.  **VPC Reachability Analyzer:**
    * Set Source (VPC-A Instance) and Destination (VPC-Shared Instance).
    * It will pinpoint exactly which component (SG, Route Table, TGW) is blocking the path.
2.  **VPC Flow Logs:**
    * Enable Flow Logs on the TGW Attachment ENIs.
    * Look for `REJECT` status. If you see `REJECT`, the issue is likely a **Security Group** or **NACL**.
3.  **Check TGW Routes:**
    * Verify in the TGW Route Table console that the routes are actually listed under the "Routes" tab for each table. If a route is missing, check your **Propagations**.
