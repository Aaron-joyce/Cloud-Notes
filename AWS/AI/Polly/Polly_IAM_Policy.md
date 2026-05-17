# Amazon Polly IAM Policy Guide

Polly IAM policies control who can synthesize speech from text and manage custom lexicons.

## Common Use Cases & Required Permissions

### 1. Speech Synthesis Client
Allows an application to convert text into spoken audio in real-time.
* **Required Actions**: `polly:SynthesizeSpeech`

*Sample Snippet (Real-time synthesis):*
```json
{
  "Effect": "Allow",
  "Action": "polly:SynthesizeSpeech",
  "Resource": "*"
}
```

## Sample Policy: Voice Application Developer
This policy allows an application to synthesize speech and also read custom lexicons (which define specific pronunciation rules for the app), but prevents modifying those lexicons.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpeechSynthesisAndLexiconRead",
      "Effect": "Allow",
      "Action": [
        "polly:SynthesizeSpeech",
        "polly:GetLexicon",
        "polly:DescribeVoices"
      ],
      "Resource": "*"
    }
  ]
}
```
