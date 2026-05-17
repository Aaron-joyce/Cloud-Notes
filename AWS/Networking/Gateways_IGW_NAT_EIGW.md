# AWS Gateways: IGW, NAT Gateway, and Egress-Only IGW

When designing a VPC, you need different types of gateways to manage how traffic flows to and from the internet. This document breaks down the three primary internet-facing gateways: Internet Gateway (IGW), NAT Gateway, and Egress-Only Internet Gateway (EIGW).

---

## 1. Internet Gateway (IGW)

An Internet Gateway is a horizontally scaled, redundant, and highly available VPC component that enables communication between instances in your VPC and the internet.

*   **Protocol:** Supports both IPv4 and IPv6.
*   **Directionality:** **Bidirectional**. It allows your instances to reach out to the internet, and it allows resources on the internet to initiate a connection to your instances.
*   **Requirement:** For an instance to use an IGW, it must reside in a public subnet and possess a Public IPv4 address or an IPv6 address.
*   **Cost:** The IGW itself is free. You only pay standard AWS data transfer rates.

### Use Case Example
A web server (e.g., Nginx or Apache) hosting a public-facing website. The server needs to respond to HTTP/HTTPS requests initiated by internet users, and it also needs to download OS updates from external repositories.

### Route Table Entry
To make a subnet "public", you associate it with a route table containing this entry:
*   **IPv4 Destination:** `0.0.0.0/0`
*   **IPv6 Destination:** `::/0`
*   **Target:** `igw-0123456789abcdef0`

---

## 2. NAT Gateway

A NAT (Network Address Translation) Gateway allows instances in a **private subnet** to connect to services outside the VPC but prevents external services from initiating a connection with those instances.

*   **Protocol:** **IPv4 Only**. (AWS recently introduced NAT64, but traditionally NAT is strictly an IPv4 concept).
*   **Directionality:** **Unidirectional** (for connection initiation). Instances inside the VPC can start an outbound session. The NAT Gateway tracks the state and allows the response traffic back in. However, someone on the internet cannot ping or SSH into the instance through the NAT Gateway.
*   **How it works:** The NAT Gateway sits in a *Public Subnet* and has an Elastic IP (public IP) attached to it. When private instances send traffic to the internet, the NAT Gateway replaces the instance's private source IP with its own Elastic IP before sending the traffic to the IGW.
*   **Cost:** You are charged an hourly rate for the NAT Gateway to exist, plus a per-GB data processing fee.

### Use Case Example
A fleet of backend application servers or database servers in a private subnet. They should never be exposed to the public internet for security reasons, but they need outbound internet access to download software patches or communicate with third-party APIs (like Stripe, Twilio, or GitHub).

### Route Table Entry
You place this entry in the route table associated with your *Private Subnet*:
*   **Destination:** `0.0.0.0/0`
*   **Target:** `nat-0123456789abcdef0`

*(Note: The NAT Gateway's own subnet must have a route to the IGW to function).*

---

## 3. Egress-Only Internet Gateway (EIGW)

An Egress-Only Internet Gateway provides outbound internet access for **IPv6** traffic while preventing inbound connections initiated from the internet.

*   **Protocol:** **IPv6 Only**.
*   **Directionality:** **Unidirectional** (for connection initiation).
*   **Why it exists:** Unlike IPv4, which relies on private ranges (like `10.x.x.x`) and NAT to conserve addresses, **all IPv6 addresses are globally routable (public)**. Because NAT is unnecessary for IPv6, you need a different mechanism to prevent the internet from reaching your instances. The EIGW acts as a stateful firewall at the edge of your VPC, blocking incoming session requests while allowing outbound ones.
*   **Cost:** The EIGW itself is free. You only pay standard AWS data transfer rates.

### Use Case Example
You have a dual-stack VPC (IPv4 and IPv6 enabled). Your private database instances are assigned globally routable IPv6 addresses. You want them to be able to download updates over the IPv6 internet, but you must guarantee that no malicious actor on the internet can initiate a connection to them using their public IPv6 address. 

### Route Table Entry
You place this entry in the route table associated with the subnet holding your IPv6 instances:
*   **Destination:** `::/0` (The IPv6 equivalent of 0.0.0.0/0)
*   **Target:** `eigw-0123456789abcdef0`

---

## 4. Summary Comparison

| Feature | Internet Gateway (IGW) | NAT Gateway | Egress-Only IGW (EIGW) |
| :--- | :--- | :--- | :--- |
| **Primary Protocol** | IPv4 & IPv6 | IPv4 | IPv6 |
| **Connection Initiation** | Bidirectional (Inbound & Outbound) | Outbound Only | Outbound Only |
| **Target Audience** | Resources in Public Subnets | Resources in Private Subnets | Resources with IPv6 addresses |
| **Subnet Placement** | Attached directly to the VPC | Deployed inside a Public Subnet | Attached directly to the VPC |
| **Address Translation?** | No (1:1 mapping for EIPs) | Yes (Many to 1) | No (IPv6 is globally routable) |
| **Cost** | Free (data transfer applies) | Hourly + Per GB Processing | Free (data transfer applies) |
