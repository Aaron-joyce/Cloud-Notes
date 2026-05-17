# Amazon Fraud Detector IAM Policy Guide

Fraud Detector IAM policies control who can build models/rules and who can send events for risk evaluation.

## Common Use Cases & Required Permissions

### 1. Fraud Evaluation Client
Allows an application (like a checkout service) to send transaction details to get a fraud prediction in real-time.
* **Required Actions**: `frauddetector:GetEventPrediction`

*Sample Snippet (Getting a prediction):*
```json
{
  "Effect": "Allow",
  "Action": "frauddetector:GetEventPrediction",
  "Resource": "*"
}
```

## Sample Policy: Fraud Rules Administrator
This policy allows a risk analyst to view models and update the business rules that determine how a prediction is handled, but prevents them from deleting or training the underlying models.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRuleManagement",
      "Effect": "Allow",
      "Action": [
        "frauddetector:CreateRule",
        "frauddetector:UpdateRuleVersion",
        "frauddetector:Get*",
        "frauddetector:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```
