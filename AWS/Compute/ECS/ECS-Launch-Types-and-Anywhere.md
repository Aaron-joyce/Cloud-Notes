# ECS Launch Types and ECS Anywhere

When running containerized workloads on Amazon Elastic Container Service (ECS), you have a few options for how the underlying compute infrastructure is managed. This documentation covers the two main launch types, as well as ECS Anywhere.

## Launch Types

### EC2 Launch Type
A traditional model where you manage the underlying EC2 instances, giving you full control over OS configurations, patching, and custom instance types.

- **Pros**: 
  - Complete control over the infrastructure (custom AMIs, instance types, e.g., GPU instances).
  - Can be more cost-effective if you have predictable workloads and can utilize Reserved Instances or Spot Instances efficiently.
- **Cons**: 
  - Requires operational overhead: you must handle OS patching, security updates, scaling the instances, and managing cluster capacity.
- **How it works**: You register EC2 instances to an ECS cluster by running the ECS container agent on them. Tasks are then scheduled onto these instances.

**CLI Commands:**
```bash
# Note: Tasks using the EC2 launch type are run similar to Fargate, but specify the EC2 launch type
aws ecs run-task \
    --cluster my-ecs-cluster \
    --task-definition my-task-def:1 \
    --launch-type EC2

# To scale the underlying instances, you typically configure an Auto Scaling Group (ASG) and link it to an ECS Capacity Provider.
```

### AWS Fargate Launch Type
A serverless compute engine for containers where AWS fully manages the underlying infrastructure, allowing you to pay only for resources allocated per task.

- **Pros**:
  - No servers to manage, patch, or secure.
  - Seamless scaling: you just specify CPU and memory requirements, and Fargate provisions the exact compute you need.
  - Built-in isolation at the task level.
- **Cons**:
  - Slightly higher base cost compared to fully optimized EC2 instances.
  - Less control over the host environment (e.g., cannot run privileged containers or access the underlying host OS).

**CLI Commands:**
```bash
# Run a task using the Fargate launch type
aws ecs run-task \
    --cluster my-ecs-cluster \
    --task-definition my-task-def:1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-67890],assignPublicIp=ENABLED}"
```

## ECS Anywhere
An extension that allows you to manage on-premises container workloads using the standard AWS ECS control plane via the Systems Manager (SSM) agent.

- **Use Cases**: Data compliance requirements that mandate data staying on-premises, low latency requirements for local processing, or leveraging existing hardware investments.
- **How it works**: You install the ECS agent and AWS Systems Manager (SSM) agent on your own on-premises servers (bare metal or VMs). They register as external instances in your ECS cluster. The ECS control plane stays in the AWS cloud, but the tasks run locally on your hardware.

**CLI Commands:**
```bash
# Register an external instance (requires an activation code from SSM)
# You generate the activation script in the console or CLI, which installs the necessary agents on your on-prem server.

# Once registered, you can list the instances in your cluster
aws ecs list-container-instances --cluster my-ecs-anywhere-cluster

# Run a task on your on-premises hardware by using the EXTERNAL launch type
aws ecs run-task \
    --cluster my-ecs-anywhere-cluster \
    --task-definition my-local-task-def:1 \
    --launch-type EXTERNAL
```
