# Amazon VPC Lattice

Amazon VPC Lattice is a fully managed application networking service built directly into the AWS network infrastructure. It provides a consistent way to connect, secure, and monitor communication between your services.

You can think of VPC Lattice as a **network-layer Service Mesh**. Traditionally, building a microservices architecture across multiple VPCs or accounts required complex networking setups—managing Transit Gateways, VPC Peering, handling overlapping IP addresses, and configuring sidecar proxies (like Envoy or Istio). VPC Lattice abstracts all this underlying network complexity away, allowing developers to focus purely on service-to-service communication.

---

## Key Concepts and Related Services

To understand VPC Lattice, you must understand its core hierarchical components:

1. **Service Network:** The highest level logical boundary. It acts as a central hub that groups together clients (VPCs) and the Services they want to consume.
2. **Service:** An independently deployable unit of software (e.g., an API, a microservice). When you create a Lattice Service, AWS generates a unique DNS endpoint for it.
3. **Listeners & Rules:** Similar to Application Load Balancers (ALBs). A listener checks for connection requests on specific ports/protocols (HTTP/HTTPS). Rules determine how to route that traffic based on paths, headers, or HTTP methods.
4. **Lattice Target Groups:** The actual backend compute resources that run your application code.

### What are Lattice Target Groups?
Lattice Target Groups are collections of compute resources (targets) that process the incoming requests. When a rule in your Lattice Service is matched, it forwards the traffic to a Target Group.
*   **Supported Targets:** 
    *   Amazon EC2 Instances
    *   IP Addresses (useful for on-premises or container workloads)
    *   AWS Lambda Functions
    *   Application Load Balancers (ALBs)

---

## What is it used for?

1. **Simplifying Cross-VPC and Cross-Account Networking:** 
   Lattice completely bypasses the need for complex network routing. **Crucially, Lattice works perfectly even if the VPCs have identical, overlapping CIDR blocks.** It performs automatic network address translation (NAT) behind the scenes.
2. **Modernizing Microservices (Without Sidecars):** 
   It provides service discovery, advanced Layer 7 load balancing (routing based on HTTP headers/paths), and observability out of the box, without requiring you to manage complex proxy fleets.
3. **Implementing Zero-Trust Security:** 
   VPC Lattice integrates natively with AWS IAM. You can apply Auth Policies to a Service Network or an individual Service, enforcing strict, identity-based access controls (e.g., "Only the `Billing-App-Role` can send an HTTP POST to the `Payment-Service`").

---

## How does it work?

When a client wants to communicate with a service using VPC Lattice:
1. The client looks up the Lattice Service's DNS name.
2. The DNS resolves to a special set of **link-local IP addresses** (managed internally by AWS, typically in the `169.254.171.x` range).
3. When the client sends the HTTP/HTTPS request, it hits the VPC boundary. The VPC Lattice data plane intercepts the traffic.
4. Lattice evaluates the routing rules and checks the IAM Auth policies.
5. If allowed, Lattice magically delivers the traffic directly to the Target Group in the destination VPC, regardless of where that VPC lives or what its IP range is.

---

## Step-by-Step Setup of a VPC Lattice

Setting up VPC Lattice involves working from the "backend compute" up to the "network hub", and finally connecting the clients.

### Step 1: Create the Target Groups
You must define where the traffic will ultimately go.
1. Go to the VPC Console -> **Target groups** (under VPC Lattice).
2. Choose a target type (Instances, IP addresses, Lambda, or ALB).
3. Configure health checks (if using Instances/IPs/ALB).
4. Register the specific targets (e.g., select your EC2 instances or Lambda function).

### Step 2: Create the VPC Lattice Service
1. Go to **Services** (under VPC Lattice) and click **Create service**.
2. Give the service a name (e.g., `inventory-api`).
3. Set up **Listeners** (e.g., HTTP on port 80).
4. Set up **Routing Rules**. For example:
   * *If Path is exactly `/api/v1/stock` -> Forward to `TargetGroup-V1`*
   * *Default action -> Return HTTP 404*

### Step 3: Create a Service Network
1. Go to **Service networks** and click **Create service network**.
2. Give it a name (e.g., `Corporate-Core-Network`).
3. **Security:** You can optionally attach an AWS IAM policy here to enforce authentication and authorization (Zero-Trust).

### Step 4: Associate the Service with the Service Network
1. In the Service Network you just created, go to the **Services** tab.
2. Click **Associate service** and select the Lattice Service you built in Step 2.
*Now, the service is officially part of the network, but no clients can reach it yet.*

### Step 5: Associate the Client VPCs with the Service Network
This is how you grant clients access to the hub.
1. In the Service Network, go to the **VPC associations** tab.
2. Click **Create VPC association**.
3. Select the VPC(s) where your client applications (the ones making the requests) live. 
4. Select the Security Groups to apply to the Lattice endpoints in the client VPC.

### Step 6: Invoke the Service
1. Obtain the generated DNS name of your Lattice Service (e.g., `inventory-api-0123456abcdef.7d67968.vpc-lattice-svcs.us-east-1.on.aws`).
2. Log into a client instance in the associated VPC.
3. Make an HTTP request to the endpoint (e.g., `curl http://inventory-api-0123456abcdef.../api/v1/stock`).
4. *Important Security Note:* Ensure the Security Group attached to your client instance allows Outbound traffic on the necessary ports (80/443) so it can reach the Lattice link-local IPs!
