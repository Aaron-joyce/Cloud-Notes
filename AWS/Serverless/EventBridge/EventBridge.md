# Amazon EventBridge

Amazon EventBridge is a serverless event bus that makes it easier to build event-driven applications at scale using events generated from your applications, integrated SaaS applications, and AWS services.

## 1. Core Event Routing Infrastructure

### Event Buses
- **Default Event Bus**: Receives events from AWS services automatically.
- **Custom Event Buses**: Used to receive and route custom events emitted by your own applications.
- **SaaS Partner Event Buses**: Dedicated buses to receive events directly from integrated SaaS partners (like Datadog, Zendesk).

### Event Patterns and JSON Content-Based Filtering
EventBridge routes events based on rules. A rule contains an Event Pattern, which is a JSON structure that matches specific fields in the incoming event payload.

### Rules Engine & Multi-Target Parallel Routing
When a rule matches an event, the Rules Engine routes the event to one or more configured targets (up to 5 targets per rule) in parallel, such as AWS Lambda, Step Functions, or SQS.

## 2. Advanced Integration Mechanics

### Amazon EventBridge Pipes
A feature to create point-to-point integrations between event producers and consumers without writing glue code. It follows a pipeline pattern:
- **Source** (e.g., DynamoDB Stream) -> **Filter** -> **Enrich** (e.g., call a Lambda function) -> **Target** (e.g., SQS queue).

### EventBridge Scheduler
A serverless scheduler that allows you to create, run, and manage scheduled tasks at scale. It supports Cron expressions, rate expressions, and one-time tasks, with universal SDK integration to invoke almost any AWS API directly.

### API Destinations
Allows you to route EventBridge events to external, third-party HTTP endpoints outside of AWS. EventBridge handles the built-in authentication (OAuth, Basic, API Keys) and delivery retries.

## 3. Event Management & Governance

### Event Schema Registry & Code Bindings Generation
A registry that stores event structure definitions (schemas). You can generate strong-typed code bindings (e.g., in Java, Python, TypeScript) directly from these schemas to use in your IDE.

### Schema Discovery
When enabled on an active event bus, Schema Discovery automatically monitors the events passing through the bus, infers their JSON schemas, and adds them to your Schema Registry.

### Event Archive and Replay
You can configure an Archive to store a historical record of events routed through a bus. Later, you can initiate a Replay to push past events back onto the bus for reprocessing (useful for debugging or recovering from application errors).
