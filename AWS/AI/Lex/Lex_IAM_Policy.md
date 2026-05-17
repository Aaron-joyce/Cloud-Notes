# Amazon Lex IAM Policy Guide

Lex IAM policies dictate who can build the chatbots (intents, slots) and who can converse with them.

## Common Use Cases & Required Permissions

### 1. Chat Client
Allows a user or frontend application to send text or voice to a bot and receive a response.
* **Required Actions**: `lex:RecognizeText`, `lex:RecognizeUtterance`

*Sample Snippet (Sending text to a bot):*
```json
{
  "Effect": "Allow",
  "Action": "lex:RecognizeText",
  "Resource": "arn:aws:lex:us-east-1:123456789012:bot-alias/MYBOTID/MYALIASID"
}
```

## Sample Policy: Bot Developer
This policy allows a developer to create and build the bot, but restricts the Lambda functions (for fulfillment) they are allowed to attach to the bot via `iam:PassRole` or resource policies.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowBotBuilding",
      "Effect": "Allow",
      "Action": [
        "lex:CreateBot",
        "lex:CreateIntent",
        "lex:CreateSlot",
        "lex:BuildBotLocale",
        "lex:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```
