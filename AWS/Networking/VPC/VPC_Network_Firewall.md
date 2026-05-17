# AWS Network Firewall

Amazon VPC Network Firewall is a managed, highly available, stateful network firewall and intrusion prevention service (IPS) for your Virtual Private Cloud (VPC). 

While Security Groups and Network ACLs provide basic Layer 3/Layer 4 traffic filtering (IPs and Ports), the AWS Network Firewall provides deep packet inspection (DPI), Layer 7 filtering (Domains/URLs), and advanced threat protection using Suricata-compatible rules.

---

## What is it used for?

AWS Network Firewall is used for advanced network security, compliance enforcement, and traffic inspection. Common use cases include:

1. **Intrusion Prevention System (IPS):** Inspecting the actual payload of network packets to detect and block active vulnerability exploits, malware, or suspicious activity patterns.
2. **Advanced Egress (Outbound) Filtering:** Ensuring that instances can only reach approved internet destinations. For example, blocking all outbound traffic except for connections to `*.github.com` or specific API endpoints.
3. **Centralized Traffic Inspection:** In a multi-VPC environment (often using AWS Transit Gateway), routing all inbound, outbound, and inter-VPC traffic through a central "Inspection VPC" that houses the Network Firewall.
4. **Protocol Enforcement:** Ensuring that traffic running over port 443 is actually TLS/SSL and not another protocol trying to sneak out over an open port.

---

## Core Components and Associated Policies

To understand how it works, you must understand its three hierarchical components:

### 1. Rule Groups
Rule groups contain the actual logic and conditions for evaluating traffic.
*   **Stateless Rule Groups:** Evaluates individual packets in isolation, without understanding the broader connection state (similar to a NACL). It is very fast. Actions can be *Pass*, *Drop*, or *Forward to Stateful rules*.
*   **Stateful Rule Groups:** Evaluates traffic within the context of a connection. It can perform deep packet inspection. You can write rules based on 5-tuples (Source/Dest IP, Source/Dest Port, Protocol), Domain lists (Allow/Deny specific URLs), or custom Suricata IPS signatures.

### 2. Firewall Policy
A Firewall Policy is a reusable configuration document. You attach your various Stateless and Stateful Rule Groups to a Firewall Policy. 
*   It also defines the **Default Actions**. For example, you can tell the policy: *"If a packet doesn't match any of my Stateless rules, forward it to the Stateful engine for deeper inspection."*

### 3. The Firewall
The actual resource deployed into your VPC. It applies the Firewall Policy to the traffic routed to it.

---

## How to Set It Up (Step-by-Step)

Setting up an AWS Network Firewall requires careful planning of your VPC routing. **Unlike Security Groups, the firewall does not automatically inspect traffic; you must use Route Tables to force traffic through the firewall endpoints.**

### Step 1: Prepare Your Network (Subnetting)
The firewall is not a gateway; it acts as a bump-in-the-wire. It requires dedicated subnets.
1. Create a dedicated **Firewall Subnet** in each Availability Zone where you want protection. 
2. *Important:* Do not deploy EC2 instances or other resources into these firewall subnets.

### Step 2: Create Rule Groups
1. Go to the **VPC Console** -> **Network Firewall** -> **Rule groups**.
2. Create your rules. For example, create a Stateful Rule Group using a "Domain list" to explicitly ALLOW traffic only to `.amazon.com`.

### Step 3: Create a Firewall Policy
1. Go to **Firewall policies** and click **Create firewall policy**.
2. Give it a name and associate the Rule Groups you created in Step 2.
3. Define your default actions (e.g., default stateful action = Drop all traffic that doesn't match a rule).

### Step 4: Create the Firewall
1. Go to **Firewalls** and click **Create firewall**.
2. Select your VPC and select the dedicated Firewall Subnets you created in Step 1.
3. Attach the Firewall Policy you created in Step 3.
4. Once created, AWS will generate **Firewall Endpoint IDs** (VPC Endpoints) in those dedicated subnets. You will need these for the next step.

### Step 5: Update Route Tables (The Critical Step)
You must manipulate route tables to route traffic out of your subnets, into the firewall, and then out to the internet (and vice versa).

**Scenario: Protecting a Public Subnet**
To force traffic between the Internet Gateway (IGW) and your public instances through the firewall, you need three separate route tables:

1. **IGW Route Table (Ingress Routing):**
   *   You attach a route table directly to the Internet Gateway.
   *   **Route:** Destination `[Your Public Subnet CIDR]` -> Target `[Firewall Endpoint ID]`. 
   *   *(Forces inbound internet traffic into the firewall).*
2. **Public Subnet Route Table:**
   *   Attached to the subnet holding your EC2 instances.
   *   **Route:** Destination `0.0.0.0/0` -> Target `[Firewall Endpoint ID]`.
   *   *(Forces outbound instance traffic into the firewall).*
3. **Firewall Subnet Route Table:**
   *   Attached to the dedicated firewall subnet.
   *   **Route:** Destination `0.0.0.0/0` -> Target `[Internet Gateway]`.
   *   *(Allows the firewall to send approved outbound traffic to the internet).*

### Step 6: Configure Logging
To monitor alerts and traffic:
1. Go to your Firewall details page.
2. Under **Firewall details**, configure logging.
3. Send **Alert logs** (when a rule explicitly blocks/alerts on traffic) and/or **Flow logs** (standard connection logging) to CloudWatch Logs, Amazon S3, or Kinesis.
