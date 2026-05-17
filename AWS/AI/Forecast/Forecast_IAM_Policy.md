# Amazon Forecast IAM Policy Guide

Forecast IAM policies control access to uploading data, training predictors, and generating forecasts.

## Common Use Cases & Required Permissions

### 1. Forecast Query Client
Allows an application to query a generated forecast for a specific item.
* **Required Actions**: `forecast:QueryForecast`

*Sample Snippet (Querying a forecast):*
```json
{
  "Effect": "Allow",
  "Action": "forecast:QueryForecast",
  "Resource": "arn:aws:forecast:us-east-1:123456789012:forecast/MyProductForecast"
}
```

## Sample Policy: Forecast Modeler
This policy allows a user to import data and train predictors, but relies on `iam:PassRole` to allow Forecast to read the raw data from S3.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowForecastModeling",
      "Effect": "Allow",
      "Action": [
        "forecast:CreateDataset",
        "forecast:CreateDatasetImportJob",
        "forecast:CreatePredictor",
        "forecast:CreateForecast",
        "forecast:Describe*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowPassRoleToForecast",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/ForecastS3Role",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "forecast.amazonaws.com"
        }
      }
    }
  ]
}
```
