# Amazon SQS (Simple Queue Service)

Amazon SQS is a fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.

## 1. Queue Types & Core Properties

### Standard Queues vs. FIFO Queues
- **Standard Queues**: Provide maximum throughput, best-effort ordering, and at-least-once delivery. Use when throughput is critical and your application can handle out-of-order or duplicate messages.
- **FIFO Queues**: Designed to enhance messaging between applications when the order of operations and events is critical, or where duplicates can't be tolerated. 

### At-Least-Once vs. Exactly-Once Delivery
- **At-Least-Once (Standard)**: A message is delivered at least once, but occasionally, more than one copy of a message is delivered.
- **Exactly-Once (FIFO)**: A message is delivered once and remains available until a consumer processes and deletes it. Duplicates are not introduced into the queue.

### Best-Effort Ordering vs. Strict First-In-First-Out Ordering
- **Best-Effort Ordering (Standard)**: Messages are generally delivered in the order they were sent, but this is not guaranteed.
- **Strict FIFO Ordering (FIFO)**: Messages are strictly ordered. 

### Message Deduplication ID and Message Group ID (FIFO specific)
- **Message Deduplication ID**: Used by SQS to deduplicate messages sent within a 5-minute interval.
- **Message Group ID**: The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are always processed one by one, in a strict order.

## 2. Message Lifecycle & Timing Primitives

### Visibility Timeout
The period of time during which SQS prevents other consuming components from receiving and processing a message after it has been received by one consumer. If the consumer fails to process and delete the message within this timeout, the message becomes visible to other consumers again.

### Short Polling vs. Long Polling
- **Short Polling** (ReceiveMessage default): SQS samples a subset of its servers and returns messages from only those servers.
- **Long Polling** (`WaitTimeSeconds` > 0): SQS waits until a message is available in the queue before sending a response, which reduces empty responses and false empty responses, lowering costs.

### Delay Queues vs. Message Timers
- **Delay Queues**: Let you postpone the delivery of all new messages to a queue for a number of seconds.
- **Message Timers**: Let you set an initial invisibility period for a single specific message when it is added to a queue.

### Message Retention Period
By default, a message is retained in the queue for 4 days. This can be configured from 1 minute up to 14 days.

## 3. Error Handling & Operational Scaling

### Dead-Letter Queues (DLQ) and Redrive Policies
- **DLQ**: A queue that other (source) queues can target for messages that can't be processed successfully.
- **Redrive Policy**: Specifies the `maxReceiveCount`. When the receive count for a message exceeds the maximum, SQS moves the message to the DLQ.

### Backlog Management & Maximum Message Size
- SQS has a maximum message size boundary of 256 KB native payload.
- You can monitor the `ApproximateNumberOfMessagesVisible` CloudWatch metric to scale your consumer fleets.

### Amazon SQS Extended Client Library
Allows you to send payloads larger than 256 KB (up to 2 GB) by storing the actual message payload in Amazon S3 and sending only a reference to the S3 object in the SQS message.

### SQS Queue Scaling & Batch Operations
You can use `SendMessageBatch`, `DeleteMessageBatch`, and `ChangeMessageVisibilityBatch` to perform operations on up to 10 messages simultaneously, reducing API calls and costs.
