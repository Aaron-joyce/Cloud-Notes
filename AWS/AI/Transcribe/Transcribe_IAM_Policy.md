# Amazon Transcribe IAM Policy Guide

Transcribe IAM policies govern who can start transcription jobs and manage custom vocabularies. Since Transcribe often processes audio from S3, S3 read permissions are also required.

## Common Use Cases & Required Permissions

### 1. Batch Transcription Application
Allows a service to submit audio files for processing.
* **Required Actions**: `transcribe:StartTranscriptionJob`, `transcribe:GetTranscriptionJob`

*Sample Snippet (Starting a job):*
```json
{
  "Effect": "Allow",
  "Action": "transcribe:StartTranscriptionJob",
  "Resource": "*"
}
```

## Sample Policy: Transcriber with S3 Access
This policy allows starting and checking the status of transcription jobs, while also providing the necessary S3 permissions to read the source audio file and write the resulting transcript back to S3.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowTranscriptionJobs",
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:ListTranscriptionJobs"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowS3AudioAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-audio-bucket/*",
        "arn:aws:s3:::my-transcript-bucket/*"
      ]
    }
  ]
}
```
