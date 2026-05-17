# AWS X-Ray

AWS X-Ray is a distributed request-tracing engine used to navigate, analyze, and debug microservices architectures.

## Distributed Tracing & Profiling

### Service Maps
X-Ray automatically visualizes structural dependency connections across your application. It draws a clear map showing how UI endpoints, message queues, Lambda functions, and database layers interact.

### Trace Analytics
Allows you to isolate individual request transactions as they travel through your system. This helps pinpoint precise lines of code, network latency bottlenecks, or downstream HTTP errors that are slowing down user requests.

### Log-to-Trace Correlation
Integrates directly with CloudWatch Logs. By injecting unique Trace IDs into your application logs, you can seamlessly jump from a high-level trace timeline straight to the explicit log line exception that occurred during that specific transaction.
