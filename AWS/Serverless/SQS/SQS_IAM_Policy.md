# Amazon SQS IAM Policy Guide

Like SNS and S3, SQS utilizes both Identity-Based Policies and Resource-Based Policies (Queue Policies).

## Common Use Cases & Required Permissions

### 1. Message Producer
Allows an application to send messages to the queue.
* **Required Actions**: `sqs:SendMessage`

*Sample Snippet (Sending a message):*
```json
{
  "Effect": "Allow",
  "Action": "sqs:SendMessage",
  "Resource": "arn:aws:sqs:us-east-1:123456789012:MyQueue"
}
```

### 2. Message Consumer
Allows a worker application to poll for messages and delete them once processed.
* **Required Actions**: `sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:GetQueueAttributes`

## Sample Policy: SNS to SQS Fanout (Queue Policy)
This Resource-Based Policy is attached to the SQS queue. It grants an Amazon SNS topic permission to send messages directly into this queue, which is a common pattern for event fanout.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSNSToPublish",
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:123456789012:MyTopic"
        }
      }
    }
  ]
}
```
