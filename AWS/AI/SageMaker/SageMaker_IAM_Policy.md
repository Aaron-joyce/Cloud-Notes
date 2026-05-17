# Amazon SageMaker IAM Policy Guide

IAM permissions for SageMaker govern who can use Studio/Notebooks, manage training/processing jobs, and deploy inference endpoints.

## Common Use Cases & Required Permissions

### 1. Data Scientist (Experimentation)
Allows a user to create and use SageMaker Notebooks and run training jobs.
* **Required Actions**: `sagemaker:CreateNotebookInstance`, `sagemaker:CreateTrainingJob`, `sagemaker:Describe*`
* **Additional Requirements**: `iam:PassRole` is strictly required to pass an execution role to the training job or notebook.

*Sample Snippet (Starting a training job):*
```json
{
  "Effect": "Allow",
  "Action": "sagemaker:CreateTrainingJob",
  "Resource": "arn:aws:sagemaker:us-east-1:123456789012:training-job/*"
}
```

## Sample Policy: SageMaker Model Deployer
This policy grants permissions to deploy an already trained model to an endpoint, restricting the roles they can pass to a specific SageMaker execution role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelDeployment",
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateModel",
        "sagemaker:CreateEndpointConfig",
        "sagemaker:CreateEndpoint"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowPassRoleToSageMaker",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/SageMakerExecutionRole",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "sagemaker.amazonaws.com"
        }
      }
    }
  ]
}
```
