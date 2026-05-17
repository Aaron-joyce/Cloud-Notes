# Amazon CloudFront

Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.

## 1. Global Infrastructure & Caching Primitives

### Edge Locations & Origin Shield
- **Edge Locations**: Hundreds of points of presence globally where content is cached closer to the viewer.
- **Regional Edge Caches**: Mid-tier caches that sit between the Edge Locations and your origin server to further reduce origin load.
- **Origin Shield**: An additional, centralized caching layer designed to minimize the concurrent requests hitting your origin even further.

### Time-to-Live (TTL) Configurations
Controls how long objects stay in the cache before CloudFront checks the origin for updates. You define the Minimum, Maximum, and Default TTL settings.

### Cache Policies vs. Origin Request Policies
- **Cache Policies**: Dictate exactly which headers, cookies, and query strings are included in the Cache Key (which determines if a request is a cache hit or miss).
- **Origin Request Policies**: Dictate which headers/cookies/query strings are forwarded to the origin server, *even if* they are not part of the Cache Key.

## 2. Origin Integration & Security Boundaries

### Automated Origin Failover
**Origin Groups** allow you to specify a primary and secondary origin. If the primary origin returns a 5xx error, CloudFront automatically fails over and routes the request to the secondary origin.

### S3 Access Control
- **Origin Access Control (OAC)**: The modern, secure way to restrict direct access to an S3 bucket, ensuring only CloudFront can read the data. (Supports AWS KMS and all regions).
- **Origin Access Identity (OAI)**: The legacy method for S3 isolation.

### VPC Private Origins & mTLS
- **VPC Private Origins**: CloudFront can securely connect to origins sitting inside a private VPC subnet (like an internal ALB) without exposing them to the public internet.
- **mTLS Enforcement**: CloudFront supports Mutual TLS, requiring viewers to present a valid client certificate before they are allowed to connect.

## 3. Edge Compute & Request Transformation

### Lambda@Edge vs. CloudFront Functions
- **Lambda@Edge**: Runs full Node.js or Python environments in Regional Edge caches. Ideal for complex logic, network calls, or modifying responses.
- **CloudFront Functions**: Runs lightweight JavaScript directly at the Edge locations. Designed for sub-millisecond execution times for simple tasks like header manipulation or URL rewrites.

### Lifecycle Triggers
You can execute edge code at four specific points:
1. **Viewer Request**: When CloudFront receives the request from the user.
2. **Origin Request**: Before CloudFront forwards a cache-miss to the origin.
3. **Origin Response**: When CloudFront receives the response from the origin.
4. **Viewer Response**: Before CloudFront returns the cached response to the user.

### On-the-Fly Compression
CloudFront can automatically compress files using Brotli or Gzip profiles to reduce payload size and speed up delivery.

### Staging Distributions
Allows you to test configuration changes or deploy new edge code safely using continuous deployment (e.g., routing 5% of traffic to a staging distribution using weight-based routing).

## 4. Content Protection & Media Protocols

### Private Asset Protection
- **Signed URLs**: Grants access to a single file (ideal for downloading an MP3 or PDF).
- **Signed Cookies**: Grants access to multiple restricted files simultaneously (ideal for video streaming segments).

### Access Control
- **Geographic Restriction**: Block or allow requests based on the viewer's country.
- **Token-Based IP Control**: Often implemented via AWS WAF to restrict access based on specific IP ranges.

### Protocol Support
CloudFront natively supports modern performance protocols including HTTP/3 over QUIC, persistent WebSockets, and gRPC.
