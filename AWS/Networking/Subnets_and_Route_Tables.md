# AWS Subnets and Route Tables Deep Dive

Understanding subnets and route tables is critical for designing secure, highly available, and functional networks in AWS. They define the boundaries of your network and control exactly how traffic flows within and outside of your VPC.

## 1. Subnets

A subnet is a logical subdivision of a VPC's IP address range. When you create a VPC, it spans all the Availability Zones (AZs) in the region. However, a subnet is tied to a single Availability Zone.

### Key Characteristics:
* **AZ Isolation:** Subnets cannot span multiple AZs. To achieve high availability, you deploy resources across multiple subnets in different AZs.
* **CIDR Blocks:** Subnets are assigned a subset of the VPC's CIDR block. For example, if your VPC is `10.0.0.0/16`, a subnet might be `10.0.1.0/24`.
* **Reserved IP Addresses:** AWS reserves the first four IP addresses and the last IP address in each subnet CIDR block. They cannot be assigned to instances.
    * `.0`: Network address
    * `.1`: Reserved by AWS for the VPC router
    * `.2`: Reserved by AWS for DNS
    * `.3`: Reserved by AWS for future use
    * `.255`: Network broadcast address (AWS does not support broadcast, but the address is reserved)

### Types of Subnets:
1. **Public Subnet:** The subnet's associated route table has a route directly to an Internet Gateway (IGW). Instances in this subnet can be assigned public IPs and communicate directly with the internet.
2. **Private Subnet:** The subnet's route table does not have a route to an IGW. Instances cannot be reached directly from the internet. They typically use a NAT Gateway to access the internet securely.
3. **VPN-Only / Isolated Subnet:** The subnet has no route to the internet (neither IGW nor NAT Gateway) but may have a route to a Virtual Private Gateway (VGW) for an on-premises VPN connection, or it might be entirely isolated (e.g., for high-security databases).

---

## 2. Route Tables

A route table contains a set of rules, called routes, that determine where network traffic from your subnet or gateway is directed. 

### Key Concepts:
* **Subnet Association:** Every subnet must be associated with exactly one route table. A single route table, however, can be associated with multiple subnets.
* **Main Route Table:** Every VPC comes with a default route table. If you create a new subnet and don't explicitly associate it with a custom route table, it automatically uses the Main Route Table. 
    * *Best Practice:* Leave the Main Route Table private (no IGW route) and create custom explicitly associated route tables for public subnets.
* **Custom Route Table:** A route table that you create for your VPC to explicitly control routing for specific subnets.

---

## 3. How Route Evaluation Works

When an instance sends traffic, the VPC router evaluates the route table associated with the instance's subnet. 

**Rule: Longest Prefix Match (Most Specific Route)**
AWS always routes traffic using the most specific route that matches the traffic's destination. 
* If you have a route for `10.0.0.0/16` pointing to Target A.
* And a route for `10.0.1.0/24` pointing to Target B.
* Traffic destined for `10.0.1.50` will be sent to Target B because `/24` is more specific (a smaller IP range) than `/16`.

---

## 4. Anatomy of a Route Table Entry

Each entry (route) in a route table consists of two main parts:
* **Destination:** The destination IP address range (expressed as a CIDR block) that you want traffic to reach.
* **Target:** The gateway, network interface, or connection through which to send the destination traffic.

### Common Route Table Entries Explained

Here is a breakdown of common entries you will see in an AWS Route Table:

#### A. The Local Route (VPC Internal Communication)
```text
Destination: 10.0.0.0/16 (The VPC CIDR)
Target: local
```
* **How it works:** This is the default route added to every route table automatically upon creation. It allows all resources within the VPC to communicate with each other using private IP addresses.
* **Note:** You cannot delete or modify this route. If you add additional IPv4/IPv6 CIDR blocks to the VPC, a local route is automatically added for those as well.

#### B. Internet Access via Internet Gateway (Public Subnet)
```text
Destination: 0.0.0.0/0
Target: igw-0123456789abcdef0 (Internet Gateway ID)
```
* **How it works:** `0.0.0.0/0` represents all possible IPv4 addresses (the entire internet). This rule says "If traffic is not destined for the local VPC (caught by the `local` rule), send it to the Internet Gateway." This is what makes a subnet "Public".

#### C. Internet Access via NAT Gateway (Private Subnet)
```text
Destination: 0.0.0.0/0
Target: nat-0123456789abcdef0 (NAT Gateway ID)
```
* **How it works:** Similar to the IGW route, this catches all external traffic. However, it sends it to a NAT Gateway (which resides in a public subnet). The NAT Gateway masks the private instance's IP, forwards the traffic to the IGW, and returns the response back to the private instance. This allows outbound internet access while preventing inbound connections from the internet.

#### D. VPC Peering Connection
```text
Destination: 172.31.0.0/16 (A different VPC's CIDR)
Target: pcx-0123456789abcdef0 (Peering Connection ID)
```
* **How it works:** If you have peered your VPC with another VPC (e.g., a shared services VPC with CIDR `172.31.0.0/16`), this route directs traffic destined for that remote VPC across the AWS private peering connection.

#### E. On-Premises Network via VPN/Direct Connect
```text
Destination: 192.168.1.0/24 (On-premises corporate network CIDR)
Target: vgw-0123456789abcdef0 (Virtual Private Gateway ID)
```
* **How it works:** Traffic bound for your corporate data center is routed through the Virtual Private Gateway, which manages the IPSec VPN tunnel or AWS Direct Connect link.
* **Route Propagation:** Often, these routes are not added manually. You can enable "Route Propagation" on your route table, which automatically pulls in routes advertised by your on-premises BGP router.

#### F. AWS Transit Gateway
```text
Destination: 10.0.0.0/8 (A broad range of internal corporate networks)
Target: tgw-0123456789abcdef0 (Transit Gateway ID)
```
* **How it works:** If you use a Transit Gateway as a central hub to connect multiple VPCs and on-premises networks, you route broad swaths of internal traffic to the TGW, which then maintains its own routing logic to determine the final destination.

#### G. Gateway VPC Endpoint (S3 or DynamoDB)
```text
Destination: pl-12345678 (Prefix List ID for the AWS Service, e.g., com.amazonaws.us-east-1.s3)
Target: vpce-0123456789abcdef0 (VPC Endpoint ID)
```
* **How it works:** When you create a Gateway Endpoint for S3 or DynamoDB, AWS automatically manages a "Prefix List" (a logical grouping of all public IP addresses for that service in that region) and adds it as the destination. Traffic bound for S3 will hit this route (since it's more specific than `0.0.0.0/0`) and travel over the AWS private network to the service without traversing the NAT or IGW.
