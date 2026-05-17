# Amazon Translate IAM Policy Guide

IAM permissions for Translate control who can perform translations and manage custom terminology.

## Common Use Cases & Required Permissions

### 1. Translation Client
Allows an application to translate text in real-time.
* **Required Actions**: `translate:TranslateText`

*Sample Snippet (Translating a string):*
```json
{
  "Effect": "Allow",
  "Action": "translate:TranslateText",
  "Resource": "*"
}
```

## Sample Policy: Localization Manager
This policy allows a user to perform translations and also manage custom terminology to ensure brand consistency, but prevents them from running batch translation jobs.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowTranslationAndTerminology",
      "Effect": "Allow",
      "Action": [
        "translate:TranslateText",
        "translate:ImportTerminology",
        "translate:GetTerminology",
        "translate:DeleteTerminology",
        "translate:ListTerminologies"
      ],
      "Resource": "*"
    }
  ]
}
```
