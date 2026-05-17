# ECS Storage, Scaling, and Security

Managing state, automatically adjusting capacity, and maintaining secure access boundaries are crucial when operating workloads on ECS.

## Storage

### Storage Mounts
Integration options for passing persistent data to containers using local instance storage, Amazon EBS volumes, or Amazon EFS for shared network filesystems.

- **Bind Mounts**: Ties a container directory to a directory on the underlying host instance (tied to the lifecycle of the EC2 instance).
- **Amazon EFS (Elastic File System)**: Provides a scalable, fully managed shared network file system. Tasks can mount EFS natively, allowing multiple tasks across different availability zones to read/write to the same data (great for Fargate).
- **Amazon EBS (Elastic Block Store)**: ECS can attach EBS volumes directly to tasks (especially useful for stateful workloads requiring high-performance block storage).

**CLI Commands:**
```bash
# Registering a task definition with an EFS volume
aws ecs register-task-definition --cli-input-json '{
  "family": "my-task",
  "containerDefinitions": [{
    "name": "app",
    "image": "my-app",
    "mountPoints": [{"sourceVolume": "efs-vol", "containerPath": "/mnt/data"}]
  }],
  "volumes": [{
    "name": "efs-vol",
    "efsVolumeConfiguration": {"fileSystemId": "fs-12345678"}
  }]
}'
```

## Scaling

### ECS Service Auto Scaling
The dynamic modification of the running task count using target tracking, step scaling, or scheduled policies via CloudWatch metrics.

- **Target Tracking**: The simplest method. You set a target value for a metric (e.g., maintain average CPU utilization at 70%). ECS automatically adds or removes tasks to keep the metric near the target.
- **Step Scaling**: Define alarms for when a metric breaches a threshold, and specify exactly how many tasks to add or remove based on the size of the breach.
- **Scheduled Scaling**: Adjust task counts based on predictable time schedules (e.g., scale up at 8 AM, scale down at 6 PM).

**CLI Commands:**
```bash
# Register a scalable target (Application Auto Scaling)
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --resource-id service/my-ecs-cluster/my-web-service \
    --scalable-dimension ecs:service:DesiredCount \
    --min-capacity 2 \
    --max-capacity 10

# Put a scaling policy (e.g., Target Tracking)
aws application-autoscaling put-scaling-policy \
    --service-namespace ecs \
    --resource-id service/my-ecs-cluster/my-web-service \
    --scalable-dimension ecs:service:DesiredCount \
    --policy-name cpu-tracking \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration "{ \"TargetValue\": 70.0, \"PredefinedMetricSpecification\": { \"PredefinedMetricType\": \"ECSServiceAverageCPUUtilization\" } }"
```

## Security

### IAM Roles (Execution vs. Task Role)
The critical distinction between the roles used by ECS to manage the task versus the roles used by the application inside the container.

- **Task Execution Role**: Used by the ECS container agent and Docker daemon (or Fargate infrastructure). It needs permissions to:
  - Pull container images from Amazon ECR.
  - Push log streams to Amazon CloudWatch Logs.
  - Retrieve secrets from AWS Secrets Manager or Parameter Store.
- **Task Role**: The role assumed by the container application itself. If your code needs to call AWS services, it uses this role. It needs permissions to:
  - Read/write to S3 buckets.
  - Query DynamoDB tables.
  - Publish messages to SQS/SNS.

**CLI Commands:**
```bash
# Task execution role and task role are specified when registering the task definition:
aws ecs register-task-definition --cli-input-json '{
  "family": "my-secure-task",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/myApplicationTaskRole",
  "containerDefinitions": [...]
}'
```
