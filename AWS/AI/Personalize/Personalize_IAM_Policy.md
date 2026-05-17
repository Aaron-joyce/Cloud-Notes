# Amazon Personalize IAM Policy Guide

Personalize IAM policies control the creation of datasets, training of models (solutions), and the querying of recommendations (campaigns).

## Common Use Cases & Required Permissions

### 1. Recommendation Client
Allows a frontend application or backend API to request real-time recommendations for a user.
* **Required Actions**: `personalize:GetRecommendations`

*Sample Snippet (Getting a recommendation):*
```json
{
  "Effect": "Allow",
  "Action": "personalize:GetRecommendations",
  "Resource": "arn:aws:personalize:us-east-1:123456789012:campaign/MyECommerceCampaign"
}
```

## Sample Policy: Personalize Administrator
This policy allows a data engineer to manage the entire Personalize lifecycle (creating datasets, training solutions, and deploying campaigns). It also requires `iam:PassRole` so Personalize can read training data from S3.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPersonalizeManagement",
      "Effect": "Allow",
      "Action": [
        "personalize:CreateDatasetGroup",
        "personalize:CreateDataset",
        "personalize:CreateDatasetImportJob",
        "personalize:CreateSolution",
        "personalize:CreateCampaign",
        "personalize:Describe*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowPassRoleToPersonalize",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/PersonalizeS3Role",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "personalize.amazonaws.com"
        }
      }
    }
  ]
}
```
