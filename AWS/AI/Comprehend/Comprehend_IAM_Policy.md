# Amazon Comprehend IAM Policy Guide

Comprehend IAM policies control access to natural language processing endpoints and custom NLP models.

## Common Use Cases & Required Permissions

### 1. Text Analysis Application
Allows a backend service to send text strings to Comprehend for real-time sentiment or entity analysis.
* **Required Actions**: `comprehend:DetectSentiment`, `comprehend:DetectEntities`

*Sample Snippet (Real-time sentiment check):*
```json
{
  "Effect": "Allow",
  "Action": "comprehend:DetectSentiment",
  "Resource": "*"
}
```

## Sample Policy: Custom Entity Recognizer
If you train a custom model (e.g., to recognize internal company part numbers), you can restrict access so an application can only use that specific model.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UseCustomRecognizer",
      "Effect": "Allow",
      "Action": "comprehend:DetectEntities",
      "Resource": "arn:aws:comprehend:us-east-1:123456789012:entity-recognizer/MyCustomPartNumberModel"
    }
  ]
}
```
