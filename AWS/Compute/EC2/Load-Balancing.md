# AWS Elastic Load Balancing (ELB)

Elastic Load Balancing (ELB) automatically distributes your incoming application traffic across multiple targets, such as EC2 instances, containers, and IP addresses, in one or more Availability Zones. It monitors the health of its registered targets and routes traffic only to the healthy targets.

AWS provides four types of load balancers:
1. **Application Load Balancer (ALB)**
2. **Network Load Balancer (NLB)**
3. **Gateway Load Balancer (GWLB)**
4. **Classic Load Balancer (CLB)** *(Legacy - Not recommended for new setups)*

---

## 1. Application Load Balancer (ALB)

**Layer:** Layer 7 (Application Layer - HTTP/HTTPS)

**How it's used:**
ALBs are best suited for load balancing of HTTP and HTTPS traffic. They provide advanced request routing targeted at the delivery of modern application architectures, including microservices and container-based applications.
* **Path-based routing:** Route traffic to different target groups based on the URL path (e.g., `/images` goes to one group, `/api` to another).
* **Host-based routing:** Route traffic based on the Host header (e.g., `api.example.com` vs. `web.example.com`).
* **Modern Protocols:** Full support for WebSockets and HTTP/2.
* **Security integrations:** Easily integrates with AWS WAF (Web Application Firewall) to protect against exploits and Amazon Cognito for user authentication.

### Steps to set up an ALB:
1. **Create Target Groups:**
   * Go to the EC2 Dashboard -> **Target Groups**.
   * Click **Create target group**.
   * Choose the target type (Instances, IP addresses, Lambda function, or ALB).
   * Specify a Name, Protocol (HTTP/HTTPS), Port, and the VPC.
   * Configure Health Checks (e.g., sending HTTP requests to `/health`).
   * Register your EC2 instances or IP addresses to this Target Group.
2. **Create the Load Balancer:**
   * Go to the EC2 Dashboard -> **Load Balancers** -> **Create Load Balancer**.
   * Select **Application Load Balancer**.
   * Set a Name and choose **Internet-facing** (public) or **Internal** (private).
   * Select your VPC and map it to at least two Availability Zones (select public subnets for an Internet-facing ALB).
3. **Configure Security Groups:**
   * Select or create a Security Group for the ALB that allows inbound HTTP/HTTPS traffic from your intended audience (e.g., `0.0.0.0/0` for public web apps).
4. **Configure Routing (Listeners):**
   * Set up a Listener on Port 80 (HTTP) or 443 (HTTPS).
   * For the default action, select **Forward to** and choose the Target Group you created in Step 1.
5. **Review and Create:**
   * Verify all settings and click **Create load balancer**.

---

## 2. Network Load Balancer (NLB)

**Layer:** Layer 4 (Transport Layer - TCP/UDP/TLS)

**How it's used:**
NLBs are designed for load balancing of TCP, UDP, and TLS traffic where extreme performance is required. 
* **Ultra-high performance:** Capable of handling millions of requests per second while maintaining ultra-low latencies.
* **Static IP Addresses:** NLB provides a static IP address per Availability Zone, and you can assign an Elastic IP to it. This is highly useful for clients that need to whitelist firewall rules to access your application.
* **Preserves Source IP:** By default, it preserves the client-side source IP, allowing the backend to see the original IP without needing specialized headers like `X-Forwarded-For`.

### Steps to set up an NLB:
1. **Create Target Groups:**
   * Go to the EC2 Dashboard -> **Target Groups** -> **Create target group**.
   * Choose target type (Instances or IP addresses).
   * Specify Protocol (TCP, UDP, TCP_UDP, or TLS) and Port.
   * Configure Health Checks (TCP connections or HTTP checks).
   * Register your targets (instances/IPs).
2. **Create the Load Balancer:**
   * Go to the EC2 Dashboard -> **Load Balancers** -> **Create Load Balancer**.
   * Select **Network Load Balancer**.
   * Choose **Internet-facing** or **Internal**.
   * Select VPC and Availability Zones. *Optional: Assign an Elastic IP to each subnet mapping for static public IPs.*
3. **Configure Security Groups:**
   * *(Feature Note: NLBs now support Security Groups directly).* Attach a security group to the NLB that allows the required inbound TCP/UDP ports.
4. **Configure Routing:**
   * Set up Listeners (e.g., TCP port 22 for SSH, or TCP 80 for high-performance web traffic).
   * Forward traffic to the TCP/UDP Target Group created in Step 1.
5. **Review and Create:**
   * Click **Create load balancer**.

---

## 3. Gateway Load Balancer (GWLB)

**Layer:** Layer 3 (Network Layer) & Layer 4 (Transport Layer)

**How it's used:**
GWLBs are designed specifically to deploy, scale, and manage third-party virtual appliances, such as firewalls, intrusion detection/prevention systems (IDS/IPS), and deep packet inspection systems.
* **Transparent Network Gateway:** It acts as a single gateway for routing traffic to and from the appliances.
* **GENEVE Protocol:** It encapsulates traffic using the GENEVE protocol on UDP port 6081. This ensures the original traffic payload and metadata are passed to the security appliances entirely transparently.

### Steps to set up a GWLB:
1. **Launch Virtual Appliances:**
   * Deploy your third-party firewall/appliance instances (e.g., Palo Alto, Fortinet) into your VPC.
2. **Create Target Groups:**
   * Create a Target Group with the **Protocol** set to **GENEVE** (Port 6081).
   * Register your virtual appliance instances as targets.
3. **Create the Load Balancer:**
   * Go to **Load Balancers** -> **Create Load Balancer** -> **Gateway Load Balancer**.
   * Select the VPC and subnets where your appliances reside.
   * Configure routing to forward traffic to your GENEVE target group.
4. **Create a Gateway Load Balancer Endpoint (GWLBE):**
   * Go to VPC Dashboard -> **Endpoints** -> **Create Endpoint**.
   * Select your GWLB service name.
   * Place the endpoint in the subnet whose traffic you want to inspect.
5. **Update VPC Route Tables:**
   * Modify your VPC route tables so that traffic entering your VPC (e.g., from an Internet Gateway) is explicitly routed to the GWLB Endpoint for inspection before reaching the final destination (like a web server subnet).

---

## 4. Classic Load Balancer (CLB)
**Layer:** Layer 4 & Layer 7

**How it's used:**
CLBs are the legacy load balancers. They provide basic load balancing across multiple Amazon EC2 instances and operate at both the request level and connection level. 
* **Note:** AWS strongly recommends migrating from CLB to ALB or NLB. CLB does not support modern features like Host-based routing, Server Name Indication (SNI), or WebSockets as robustly as the newer generation load balancers. Setup steps are generally omitted for new architectures as it is considered deprecated.
