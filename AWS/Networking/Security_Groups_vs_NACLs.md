# Security Groups and Network ACLs (NACLs)

In AWS, you control network traffic to and from your resources using two primary firewall mechanisms: Security Groups and Network Access Control Lists (NACLs). While they seem similar, they operate at different layers and have distinct behaviors.

## What are they?

### Security Groups (SGs)
A Security Group acts as a virtual firewall at the **instance level**. You attach it directly to specific AWS resources (like EC2 instances, RDS databases, or Application Load Balancers) to control inbound and outbound traffic for that specific resource.

### Network Access Control Lists (NACLs)
A Network ACL acts as a virtual firewall at the **subnet level**. You associate it with a subnet, and it controls all traffic entering and exiting that entire subnet, acting as a perimeter border defense before traffic even reaches the instances inside.

---

## How are they different?

| Feature | Security Group (SG) | Network ACL (NACL) |
| :--- | :--- | :--- |
| **Scope** | Instance Level (Attached to ENIs) | Subnet Level |
| **Statefulness** | **Stateful:** If you send a request outward, the response is automatically allowed inward, regardless of inbound rules. | **Stateless:** Return traffic must be explicitly allowed by inbound/outbound rules. |
| **Rule Types** | **Allow Only:** All rules are "allow". Whatever is not explicitly allowed is denied by default. | **Allow and Deny:** You can create both allow rules and explicit deny rules (e.g., block a specific IP). |
| **Rule Evaluation** | **All rules evaluated:** AWS evaluates all rules before deciding whether to allow traffic. | **Order of evaluation:** Rules are evaluated in numerical order (lowest to highest). The first matching rule applies. |
| **Default Behavior** | **Default SG:** Allows all inbound from instances in the same SG, allows all outbound. <br>**New SG:** Denies all inbound, allows all outbound. | **Default NACL:** Allows all inbound and outbound traffic. <br>**New Custom NACL:** Denies all inbound and outbound traffic. |

---

## Can they be used together?

**Yes.** In fact, using them together is an AWS best practice to achieve "Defense in Depth". 

When traffic flows from the internet to your EC2 instance, it must first pass through the NACL (the perimeter fence). If the NACL allows it, the traffic then hits the Security Group (the building's front door). If both allow the traffic, it reaches the instance. 

* SGs are generally used for your day-to-day application logic (e.g., "Allow web traffic to the web tier, allow web tier to talk to the database tier").
* NACLs are generally used for broad security strokes (e.g., "Block this known malicious IP block from accessing any part of our network").

---

## Example: Using Both Together

**The Scenario:** You have a Web Server in a Public Subnet. It needs to serve HTTP (80) and HTTPS (443) traffic to the internet. However, your security team has identified a malicious IP address (`203.0.113.50`) that is attacking your servers, and you need to block it entirely.

Because Security Groups *cannot* contain "Deny" rules, you cannot use an SG to block the specific IP. You must use a NACL to block the attacker, and an SG to allow the web traffic.

### 1. Security Group Setup (Attached to the EC2 Web Server)
The Security Group focuses only on what the server is supposed to do.

*   **Inbound Rules:**
    *   Allow HTTP (Port 80) from `0.0.0.0/0`
    *   Allow HTTPS (Port 443) from `0.0.0.0/0`
*   **Outbound Rules:**
    *   Allow All Traffic to `0.0.0.0/0` (Default setting, allows the server to fetch updates)

*Because SGs are stateful, when a user sends an HTTP request, the server's response is automatically allowed out, regardless of the outbound rules.*

### 2. NACL Setup (Associated with the Public Subnet)
The NACL focuses on the perimeter defense and requires careful handling of "Stateless" traffic via ephemeral ports. When a client connects to port 80, they initiate the connection from a random high-numbered port (e.g., port 54321). The NACL must explicitly allow the server's response to go back to that high port.

*   **Inbound Rules:**
    *   `Rule 100:` **DENY** ALL Traffic from `203.0.113.50/32` *(This stops the malicious IP. Evaluation stops here for that IP).*
    *   `Rule 200:` **ALLOW** HTTP (80) from `0.0.0.0/0` *(Allows normal web traffic in).*
    *   `Rule 210:` **ALLOW** HTTPS (443) from `0.0.0.0/0` *(Allows normal web traffic in).*
    *   `Rule 220:` **ALLOW** Custom TCP (Ports 1024-65535) from `0.0.0.0/0` *(Allows inbound return traffic if the server initiates an outbound request, like downloading a patch).*
    *   `Rule * :` DENY ALL *(Implicit default).*

*   **Outbound Rules:**
    *   `Rule 100:` **ALLOW** HTTP (80) to `0.0.0.0/0` *(Allows the server to make outbound HTTP requests).*
    *   `Rule 110:` **ALLOW** HTTPS (443) to `0.0.0.0/0` *(Allows the server to make outbound HTTPS requests).*
    *   `Rule 120:` **ALLOW** Custom TCP (Ports 1024-65535) to `0.0.0.0/0` *(CRITICAL: Allows the server to send responses back to the users who connected on inbound port 80/443).*
    *   `Rule * :` DENY ALL *(Implicit default).*

### Why this works:
1. The malicious IP hits the NACL on inbound `Rule 100`. It is explicitly denied. It never even reaches the Security Group.
2. A normal user hits the NACL. `Rule 100` doesn't match. `Rule 200` matches and allows them in.
3. The normal user's traffic then hits the Security Group. The SG Inbound rule for Port 80 allows them in.
4. The server processes the request and sends the webpage back.
5. The SG automatically allows the response out (Stateful).
6. The NACL Outbound `Rule 120` explicitly allows the response out to the user's ephemeral port (Stateless).
