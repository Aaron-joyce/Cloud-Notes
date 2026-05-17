# ECS Deployment & Service Discovery

Managing how new versions of applications are rolled out and how services communicate with each other are critical components of running production workloads on ECS.

## Deployment Strategies

### Rolling Update Deployment
The default update strategy where ECS gradually replaces old tasks with new ones based on minimum and maximum healthy percent boundaries.

- **How it works**: ECS starts new tasks based on a new task definition revision. Once the new tasks are healthy and passing load balancer health checks, it begins draining and terminating the old tasks.
- **Controls**:
  - `minimumHealthyPercent`: The lower limit on the number of tasks that must remain running during an update (e.g., 50%).
  - `maximumPercent`: The upper limit on the number of tasks that can run during an update (e.g., 200%).

**CLI Commands:**
```bash
# Update a service to use a rolling update strategy (implicit default)
# and force a new deployment
aws ecs update-service \
    --cluster my-ecs-cluster \
    --service my-web-service \
    --force-new-deployment
```

### Blue/Green Deployment (via AWS CodeDeploy)
A deployment model that shifts traffic from an old version of your service to an entirely new stack using a load balancer to minimize downtime.

- **How it works**: CodeDeploy provisions a "green" set of tasks alongside the active "blue" set. Traffic is routed via a load balancer (ALB or NLB). Once the green tasks are verified as healthy, traffic is fully or linearly shifted over to them, and the blue tasks are eventually terminated.
- **Benefits**: Near-zero downtime, easy rollbacks (just shift traffic back to the blue target group).

**CLI Commands:**
```bash
# Blue/Green deployments are typically managed via CodeDeploy rather than directly through ECS CLI.
# You create a CodeDeploy application and deployment group.
aws deploy create-deployment \
    --application-name my-ecs-app \
    --deployment-group-name my-ecs-dg \
    --revision revisionType=AppSpecContent,appSpecContent={content='string'}
```

## Service Discovery & Connectivity

### Service Connect
A cloud-native service mesh feature providing service-to-service discovery, traffic management, and secure communication inside clusters without configuring external discovery tools.

- **How it works**: ECS deploys an Envoy proxy as a sidecar container in your tasks. This proxy intercepts and manages traffic between microservices using friendly DNS names (e.g., `backend.my-app`).
- **Benefits**: Simplified network configuration, built-in telemetry, and robust traffic routing (like retries and timeouts) without needing an external service mesh like AWS App Mesh.

**CLI Commands:**
```bash
# Update a service to enable Service Connect
aws ecs update-service \
    --cluster my-ecs-cluster \
    --service my-web-service \
    --service-connect-configuration "enabled=true,namespace=my-namespace,services=[{portName=web,clientAliases=[{port=80,dnsName=web.my-namespace}]}]"
```
