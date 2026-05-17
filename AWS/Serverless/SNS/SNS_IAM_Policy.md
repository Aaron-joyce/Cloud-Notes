# Amazon SNS IAM Policy Guide

SNS supports both Identity-Based Policies (who can manage topics) and Resource-Based Policies (Topic Policies, defining who can publish/subscribe to the topic).

## Common Use Cases & Required Permissions

### 1. Topic Publisher
Allows an application to send messages to a specific SNS topic.
* **Required Actions**: `sns:Publish`

*Sample Snippet (Publishing to a topic):*
```json
{
  "Effect": "Allow",
  "Action": "sns:Publish",
  "Resource": "arn:aws:sns:us-east-1:123456789012:MyTopic"
}
```

### 2. Cross-Account Subscription (Topic Policy)
A Resource-Based Policy attached to the SNS topic that allows an SQS queue in a *different* AWS account to subscribe to it.

## Sample Policy: Cross-Account Publish (Topic Policy)
This policy is attached directly to the SNS topic. It allows an external AWS account (`999999999999`) to publish messages to this topic.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExternalAccountPublish",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::999999999999:root"
      },
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:us-east-1:123456789012:MyTopic"
    }
  ]
}
```
