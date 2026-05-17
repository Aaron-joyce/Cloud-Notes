# Amazon Rekognition IAM Policy Guide

Rekognition uses IAM to control who can send images/videos for analysis or manage face collections.

## Common Use Cases & Required Permissions

### 1. Application Analyzer
Allows an application to call Rekognition APIs to analyze images (e.g., detecting labels or text).
* **Required Actions**: `rekognition:DetectLabels`, `rekognition:DetectText`, `rekognition:DetectFaces`

*Sample Snippet (Detecting objects in an image):*
```json
{
  "Effect": "Allow",
  "Action": "rekognition:DetectLabels",
  "Resource": "*"
}
```

## Sample Policy: Face Collection Manager
This policy allows an application to index new faces and search against a specific Face Collection, but prevents them from deleting the collection entirely.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowFaceSearchAndIndex",
      "Effect": "Allow",
      "Action": [
        "rekognition:IndexFaces",
        "rekognition:SearchFacesByImage",
        "rekognition:ListFaces"
      ],
      "Resource": "arn:aws:rekognition:us-east-1:123456789012:collection/MyEmployeeFaces"
    }
  ]
}
```
