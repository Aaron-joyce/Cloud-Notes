# AWS ECS Basics

Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that makes it easy to deploy, manage, and scale containerized applications.

## Core Concepts

### ECS Cluster
A logical grouping of compute resources (EC2 or Fargate) within an AWS Region where your containerized applications run.

- **Fargate Capacity Providers**: Serverless compute for containers. You don't have to provision or manage servers.
- **EC2 Capacity Providers**: You manage the underlying EC2 instances that the containers run on.

**CLI Commands:**
```bash
# Create an ECS cluster
aws ecs create-cluster --cluster-name my-ecs-cluster

# List clusters
aws ecs list-clusters

# Describe a cluster
aws ecs describe-clusters --clusters my-ecs-cluster
```

### Task Definition
A JSON-formatted text file/blueprint that specifies parameters like container images, CPU/memory limits, storage volumes, and environment variables.

- Acts similarly to a `docker-compose.yml` file, but designed specifically for ECS.
- Contains configuration for one or more containers (up to a maximum of 10) that should run together.
- Defines networking modes (e.g., `awsvpc`, `bridge`, `host`, `none`) and IAM roles (Task Role for the app, Task Execution Role for pulling images and pushing logs).

**CLI Commands:**
```bash
# Register a task definition from a local JSON file
aws ecs register-task-definition --cli-input-json file://task-def.json

# List active task definitions
aws ecs list-task-definitions --status ACTIVE

# Describe a specific task definition
aws ecs describe-task-definition --task-definition my-task-def:1
```

### Task
The actual runtime instantiation of a task definition, representing one or more closely linked containers running on a host.

- Represents a single running copy of your task definition.
- If your task definition specifies a web container and a Datadog agent container, one task will launch both containers on the same host (sharing the same lifecycle and network namespace if using `awsvpc`).

**CLI Commands:**
```bash
# Run a one-off task (outside of a service)
aws ecs run-task \
    --cluster my-ecs-cluster \
    --task-definition my-task-def:1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-67890],assignPublicIp=ENABLED}"

# List running tasks in a cluster
aws ecs list-tasks --cluster my-ecs-cluster

# Stop a running task
aws ecs stop-task --cluster my-ecs-cluster --task task-id-here
```

### Service
An ECS configuration that ensures the requested number of tasks are continuously running, handling task health, restarts, and optional load balancer integration.

- Maintains the **desired count** of tasks. If a task fails or an underlying EC2 instance dies, the service scheduler replaces the task automatically.
- Integrates easily with Elastic Load Balancing (Application Load Balancers or Network Load Balancers) to distribute incoming traffic evenly across the tasks.
- Manages deployments (e.g., Rolling updates, Blue/Green deployments with CodeDeploy) to safely roll out new versions of task definitions.

**CLI Commands:**
```bash
# Create an ECS service
aws ecs create-service \
    --cluster my-ecs-cluster \
    --service-name my-web-service \
    --task-definition my-task-def:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-67890]}"

# Update a service (e.g., scaling up to 4 tasks)
aws ecs update-service --cluster my-ecs-cluster --service my-web-service --desired-count 4

# Force a new deployment to pull new container images
aws ecs update-service --cluster my-ecs-cluster --service my-web-service --force-new-deployment

# Describe a service
aws ecs describe-services --cluster my-ecs-cluster --services my-web-service
```
