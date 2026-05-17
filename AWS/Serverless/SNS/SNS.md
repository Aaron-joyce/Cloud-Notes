# Amazon SNS (Simple Notification Service)

Amazon SNS is a fully managed messaging service for both application-to-application (A2A) and application-to-person (A2P) communication.

## 1. Architecture & Message Delivery Models

### Pub/Sub (Publisher/Subscriber) Paradigm
In SNS, publishers communicate asynchronously with subscribers by producing and sending a message to a topic, which is a logical access point and communication channel. Subscribers consume the messages from the topic.

### Topics (Standard vs. FIFO Topics)
- **Standard Topics**: Provide maximum throughput, best-effort ordering, and at-least-once delivery.
- **FIFO Topics**: Ensure strict message ordering and exactly-once message delivery, integrating seamlessly with SQS FIFO queues.

### Protocol Endpoints
SNS supports fanning out messages to a variety of endpoints:
- **A2A**: Amazon SQS, AWS Lambda, HTTP/S endpoints.
- **A2P**: SMS (text messages), Email, Mobile Push notifications.

### SNS Fanout Pattern
A pattern where an SNS topic publishes a message to multiple SQS queues (or other endpoints) simultaneously in parallel, allowing for independent asynchronous processing of the same event by different microservices.

## 2. Message Filtering & Transformation

### Topic Subscription Attributes
Configuration settings applied to a specific subscription, determining how SNS delivers messages to that endpoint.

### Subscriber-Side Message Filtering Policies
Instead of receiving every message published to a topic, subscribers can define filter policies based on message attributes (e.g., attribute-based string/numeric matching). SNS will only push the message to the subscriber if it matches the policy.

### Payload Delivery Optimization (Raw Message Delivery)
When "Raw Message Delivery" is toggled on, SNS delivers the exact payload published by the sender, stripping out the default JSON metadata wrapper (like `MessageId`, `Timestamp`) that SNS usually wraps around the message payload.

## 3. Reliability & Security

### Message Delivery Status Logs
You can enable delivery status logging to Amazon CloudWatch Logs to track the success or failure rates of message deliveries to endpoints like HTTP, Lambda, or SQS.

### Delivery Retry Policies
SNS defines delivery retry policies that dictate how many times and at what intervals SNS attempts to redeliver a message if the endpoint is unreachable. This includes strategies like Exponential Backoff and Linear Backfill.

### Server-Side Encryption (SSE)
You can encrypt messages stored in an SNS topic at rest using AWS KMS (Key Management Service) keys.
