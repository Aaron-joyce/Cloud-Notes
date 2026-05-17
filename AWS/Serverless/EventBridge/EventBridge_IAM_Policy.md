# Amazon EventBridge IAM Policy Guide

IAM permissions govern who can create event buses and rules, as well as who is allowed to publish events to a bus.

## Common Use Cases & Required Permissions

### 1. Event Publisher
Allows an application or service to put custom events onto an Event Bus.
* **Required Actions**: `events:PutEvents`

*Sample Snippet (Publishing events):*
```json
{
  "Effect": "Allow",
  "Action": "events:PutEvents",
  "Resource": "arn:aws:events:us-east-1:123456789012:event-bus/my-custom-bus"
}
```

### 2. Rule Administrator
Allows creating routing rules and attaching targets (like Lambda or SQS) to them.
* **Required Actions**: `events:PutRule`, `events:PutTargets`
* **Additional Requirements**: `iam:PassRole` is often needed to allow EventBridge to assume a role to invoke the target.

## Sample Policy: Event Publisher
This simple policy grants an application permission to send events only to a specific custom event bus.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPutEvents",
      "Effect": "Allow",
      "Action": "events:PutEvents",
      "Resource": "arn:aws:events:us-east-1:123456789012:event-bus/my-custom-bus"
    }
  ]
}
```
