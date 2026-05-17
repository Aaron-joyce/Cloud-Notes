# Amazon API Gateway

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale.

## 1. API Types & Protocols

### REST APIs
Feature-rich APIs providing full control over the request/response cycle, extensive authorization options, and request validation. Supports both proxy and non-proxy integrations.

### HTTP APIs
A newer, low-latency, and cost-optimized serverless-focused alternative to REST APIs. They offer up to 71% cost savings and 60% latency reduction compared to REST APIs, though with fewer advanced features.

### WebSocket APIs
Maintain stateful, bidirectional, real-time streaming connections between clients and servers. Ideal for chat applications or real-time dashboards.

## 2. Integration Types & Mapping

### Proxy Integrations (AWS_PROXY)
The easiest way to integrate with backend services like AWS Lambda. The entire client request (headers, path parameters, body) is passed directly to the backend as-is, and the backend returns the raw HTTP response.

### Custom Integrations
For non-proxy integrations, you configure exactly how the client request data is mapped to the backend format, and how the backend response is mapped back to the client.

### Apache Velocity Template Language (VTL)
Used in custom integrations to define Data Mapping Templates. VTL allows you to transform the JSON payload of the request before it hits the backend, or transform the response before it returns to the client.

## 3. Security, Access Control, and Authorization

### IAM Policies & Resource Policies
You can control access to APIs using standard AWS IAM permissions or attach Resource Policies directly to the API Gateway to restrict access by IP range or VPC endpoint.

### Custom Lambda Authorizers
A Lambda function you provide to control access to your API.
- **Token-based**: Receives the caller's identity in a bearer token (e.g., OAuth/SAML).
- **Request-parameter-based**: Receives the caller's identity in a combination of headers, query string parameters, stageVariables, and $context variables.

### Amazon Cognito User Pools Integration
Built-in integration to authenticate API calls using JSON Web Tokens (JWTs) issued by Amazon Cognito.

### API Keys, Usage Plans, and Client Certificates
- **API Keys & Usage Plans**: Used to throttle and set quotas on third-party developers accessing your API.
- **Client Certificates**: Ensure that the backend system (e.g., on-premises server) only accepts requests coming securely from API Gateway.

## 4. Traffic Management & Performance

### Throttling Settings
API Gateway protects backends by applying a Token Bucket algorithm to throttle requests. This can be configured at the Account level or overridden at the Route/Method level.

### API Gateway Caching
You can enable a TTL-based staging cache to store responses from your endpoint. This reduces the number of calls made to your backend and improves latency for clients.

### Stage Variables and Canary Deployments
- **Stage Variables**: Name-value pairs that act like environment variables for API Gateway stages, allowing you to dynamically point to different backends (e.g., `dev` vs `prod` Lambda aliases).
- **Canary Deployments**: Allows you to safely roll out new API changes by directing a small percentage of traffic (e.g., 5%) to a new deployment while monitoring errors before fully cutting over.
