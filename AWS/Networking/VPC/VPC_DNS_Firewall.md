# Route 53 Resolver DNS Firewall (VPC DNS Firewall)

## What is a DNS Firewall in VPC?

Amazon Route 53 Resolver DNS Firewall is a managed security feature that protects your Virtual Private Clouds (VPCs) by filtering outbound Domain Name System (DNS) queries. 

When resources inside your VPC (like EC2 instances or Lambda functions) attempt to resolve a domain name (e.g., `www.example.com` into an IP address) using the default VPC DNS server (the Route 53 Resolver), the DNS Firewall intercepts that query. It evaluates the domain name against a set of rules you define to determine whether the query should be allowed or blocked.

---

## What is it used for?

The DNS Firewall is a critical layer in a "Defense in Depth" strategy. It is primarily used for:

1. **Preventing Data Exfiltration (DNS Tunneling):** Malicious actors often bypass standard firewalls by sneaking data out of a network embedded inside DNS queries. A DNS Firewall can block queries to unauthorized or suspicious domains, shutting down this vector.
2. **Blocking Command and Control (C&C):** If an instance in your VPC is compromised by malware, it will often try to "phone home" to an attacker's server. Blocking known malicious domains prevents the instance from receiving instructions.
3. **Enforcing "Walled Garden" (Allow-list) Environments:** In highly regulated or secure environments, you can configure the firewall to block *all* DNS queries by default, only allowing resolutions for a strictly vetted list of domains (e.g., `*.amazonaws.com` and `api.github.com`).
4. **Protection via Threat Intelligence:** Utilizing AWS Managed Domain Lists to automatically block domains associated with malware, botnets, and phishing, backed by AWS's threat intelligence.

---

## How does it work?

By default, any instance in a VPC queries the internal Route 53 Resolver (located at the `VPC CIDR + 2` IP address, like `10.0.0.2`). 

When the DNS Firewall is enabled and associated with that VPC:
1. The instance sends a DNS query for `malicious-domain.com`.
2. The Route 53 Resolver intercepts the query and checks it against your attached **Rule Groups**.
3. A Rule Group contains rules that reference **Domain Lists**. 
4. The firewall evaluates the rules in priority order (lowest number first).
5. Depending on the rule match, the firewall takes an **Action**:
   *   **ALLOW:** The Resolver fetches the IP address and returns it to the instance.
   *   **BLOCK:** The query is stopped. The firewall can respond to the instance in a few ways:
       *   `NXDOMAIN`: Tells the instance the domain does not exist.
       *   `NODATA`: Returns a successful response but with no IP address attached.
       *   `OVERRIDE`: Returns a custom CNAME or IP address, effectively "sinkholing" the request by redirecting the instance to a safe, internal server you control for analysis.
   *   **ALERT:** The query is allowed to resolve normally, but the event is logged (highly useful when first deploying rules to ensure you don't break production traffic).

---

## How to Set It Up (Step-by-Step)

Setting up a DNS Firewall involves creating lists of domains, defining rules for those lists, and attaching them to your VPC.

### Step 1: Create Domain Lists (Optional, if using custom domains)
You need lists of domains to filter against. You can use AWS Managed Lists, but if you have custom needs:
1. Go to the **VPC Console** -> **Route 53 Resolver** -> **DNS Firewall** -> **Domain lists**.
2. Click **Add domain list**.
3. Name the list (e.g., `My-Approved-APIs`) and input the domains (e.g., `api.stripe.com`, `*.github.com`).

### Step 2: Create a Rule Group
A Rule Group is the container for your firewall rules.
1. Navigate to **Rule groups** and click **Create rule group**.
2. Give it a name and description.

### Step 3: Add Rules to the Rule Group
Inside the Rule Group, you define what happens when a domain matches a list.
1. Click **Add rule**.
2. **Name the rule** and set a **Priority** (e.g., 100. Lower numbers evaluate first).
3. **Choose a Domain List:** Select either an AWS Managed list (e.g., `AWSManagedDomainsMalwareDomainList`) or a Custom list you created in Step 1.
4. **Select an Action:** Choose ALLOW, BLOCK, or ALERT.
   * *If BLOCK is selected, choose the response type (NXDOMAIN, NODATA, or Override).*
5. Repeat this process to build your logic (e.g., Rule 100 Blocks malware, Rule 200 Allows specific APIs).

### Step 4: Associate the Rule Group with a VPC
The rules do absolutely nothing until they are attached to a VPC.
1. Go to the **Associated VPCs** tab within your Rule Group.
2. Click **Associate VPC**.
3. Select the VPC(s) you want to protect.
*Once associated, all outbound DNS queries from those VPCs to the Route 53 Resolver are immediately subject to the firewall rules.*

### Step 5: Configure Logging (Highly Recommended)
To see the firewall in action:
1. Go to **Route 53 Resolver** -> **Query logging**.
2. Configure query logging for your VPC, sending the logs to CloudWatch Logs, Amazon S3, or Kinesis Data Firehose. This allows you to monitor which queries are being blocked or alerted.
