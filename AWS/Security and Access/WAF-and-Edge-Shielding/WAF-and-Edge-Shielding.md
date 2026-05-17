# AWS WAF (Web Application Firewall) & Edge Shielding

AWS WAF helps protect web applications and APIs against common web exploits and bots that may affect availability, compromise security, or consume excessive resources.

## 1. Web Access Control Lists (Web ACLs) & Components

### Web ACL Associations
Web ACLs are the core of AWS WAF. They must be associated with specific regional or global AWS resources:
- Amazon CloudFront (Global)
- Amazon API Gateway
- Application Load Balancers (ALB)
- AWS AppSync

### Rules and Rule Groups
- **AWS Managed Rules**: Pre-configured, ready-to-use rule sets curated by AWS and AWS Marketplace sellers to protect against common threats (like the OWASP Top 10).
- **Custom Rules**: Rules you write yourself to inspect specific parts of the web request.

### Match Conditions
Rules use match conditions to inspect requests. Types include:
- IP sets (allow/block specific IPs)
- Country codes (Geo-blocking)
- String/Regex matching
- SQL Injection attacks
- Cross-Site Scripting (XSS)

### Rule Actions
When a request matches a rule, the WAF can take the following actions:
- **Allow**: Let the request pass.
- **Block**: Terminate the request and return an HTTP 403 Forbidden.
- **Count**: Do not block, but count the request (useful for testing new rules).
- **Challenge**: Run a silent browser challenge to ensure the client is a browser.
- **CAPTCHA**: Present a visual/audio CAPTCHA to the user.

## 2. Traffic Mitigation & Bot Control

### Token-Bucket Rate Limiting Rules
A rule type that tracks the rate of requests for each originating IP address. If an IP exceeds the specified limit (e.g., 2000 requests per 5 minutes), the WAF temporarily blocks further requests from that IP.

### WAF Bot Control & Fraud Control
Managed rule groups specifically designed to give you visibility and control over common and pervasive bot traffic (like scrapers or scanners) and targeted fraud attempts (like account takeover or credential stuffing).

### Custom Response Bodies and HTTP Status Code Overrides
Instead of returning a standard 403 Forbidden when a request is blocked, you can configure WAF to return custom JSON/HTML responses and custom HTTP status codes (e.g., HTTP 429 Too Many Requests).

## 3. DDoS Defense (AWS Shield)

### AWS Shield Standard
A fully managed DDoS protection service that defends against most common, frequently occurring network and transport layer (Layer 3 and Layer 4) DDoS attacks. It is enabled by default for all AWS customers at no extra cost.

### AWS Shield Advanced
A paid service providing enhanced protections for larger and more sophisticated attacks, including Application Layer (Layer 7) mitigation. It also provides financial protection against DDoS-related AWS bill spikes and 24x7 access to the AWS Shield Response Team (SRT).
