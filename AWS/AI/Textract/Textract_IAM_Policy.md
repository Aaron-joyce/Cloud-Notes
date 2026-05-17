# Amazon Textract IAM Policy Guide

Textract permissions dictate who can extract data from documents. If documents are in S3, the user or service also needs S3 read permissions.

## Common Use Cases & Required Permissions

### 1. Synchronous Document Processing
Allows an application to pass a document directly in the API call and get immediate results.
* **Required Actions**: `textract:AnalyzeDocument`, `textract:DetectDocumentText`

*Sample Snippet (Extracting forms/tables):*
```json
{
  "Effect": "Allow",
  "Action": "textract:AnalyzeDocument",
  "Resource": "*"
}
```

## Sample Policy: Asynchronous Document Processing
For large multi-page PDFs, Textract uses asynchronous jobs. This policy allows starting a job and fetching the results. It requires S3 permissions to read the source file.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAsyncTextract",
      "Effect": "Allow",
      "Action": [
        "textract:StartDocumentAnalysis",
        "textract:GetDocumentAnalysis"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowS3ReadForTextract",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-document-bucket/*"
    }
  ]
}
```
