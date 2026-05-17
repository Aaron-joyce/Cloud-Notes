# AWS Mock Test & Competition Checklist

This checklist is based on the grading rubric to help ensure all criteria are met for full marks. It covers the 6 Pillars of the AWS Well-Architected Framework, plus Organization & Management.

**Note on Naming & Tagging:** 
Throughout this checklist, replace `<state>` with your actual state code. Make sure EVERY resource you create includes the tag `CompetitorId=<state_code>`.

---

## 1. Cost Optimization
- [ ] **DynamoDB Billing:** Set the `titanflow-repo-table` billing mode to `PAY_PER_REQUEST` (On-Demand).
- [ ] **ECS Fargate Sizing:** Ensure the ECS task definition specifies exactly `256 CPU units` and `512 MiB memory`.
- [ ] **API Gateway Caching:** Set the `prod` stage cache cluster size to `0.5 GB`.
- [ ] **S3 Lifecycle Rules:** Add a rule on the `titanflow-<state>-logs` bucket to transition objects to `STANDARD_IA` at 30 days, and expire (delete) them at 90 days.
- [ ] **Backup Retention:** Configure the AWS Backup plan rule retention to exactly `7 days`.
- [ ] **Compute Types:** Do NOT launch any additional EC2 instances beyond the pre-provisioned engine instance. Use ECS Fargate for your tasks.

---

## 2. Operational Excellence
- [ ] **Container Insights:** Enable Container Insights on the ECS cluster (`titanflow-<state>-cluster`).
- [ ] **ALB Logging:** Enable Application Load Balancer access logs and send them to the `titanflow-<state>-logs` S3 bucket with the prefix `alb/`.
- [ ] **VPC Flow Logs:** Enable flow logs on the default VPC and deliver them to the CloudWatch Logs group `titanflow-<state>-flowlogs`.
- [ ] **CloudWatch Dashboard (`titanflow-<state>-dashboard`):** 
  - Ensure all 4 groups are covered (ALB, ECS, DynamoDB, SQS).
  - Add *multiple* metrics per group to get full points (e.g., p50 & p99 latency for ALB; latency & request counts for ECS; provisioned/consumed capacity & throttles for DDB; queue depth & DLQ depth for SQS).
- [ ] **CloudWatch Alarms:** Create 4 specific alarms with correct metric names and namespaces:
  - [ ] ELB 5xx Errors
  - [ ] ECS CPU Utilization
  - [ ] DynamoDB Throttled Requests
  - [ ] ALB Unhealthy Host Count
- [ ] **SNS Notifications:** Ensure all 4 alarms trigger an action to the SNS topic `titanflow-<state>-alerts`.
- [ ] **SNS Subscriptions:** Verify the `titanflow-<state>-alerts` SNS topic has at least one *Confirmed* subscription.
- [ ] **X-Ray Tracing (API Gateway):** Enable active X-Ray tracing on the API Gateway `prod` stage.
- [ ] **X-Ray Group:** Create an X-Ray group named `titanflow-slow` with the filter expression: `responsetime > 1`.
- [ ] **CloudWatch Metric Filters:** Create a filter on the `/ecs/catalog-service` log group that produces a metric named `RateLimitHits` in the namespace `TitanFlow/RateLimit`.

---

## 3. Security
- [ ] **WAF Creation:** Create a WAF WebACL named `titanflow-<state>-waf` with the scope set to `REGIONAL`.
- [ ] **WAF Rate Limiting:** Add a rate-based rule to the WebACL with a limit of `1000` requests per 5-minute window, aggregated by IP.
- [ ] **WAF Managed Rules:** Add the `AWSManagedRulesCommonRuleSet` to the WebACL.
- [ ] **WAF Association:** Associate the WebACL with the API Gateway `prod` stage (Do NOT associate it with the ALB).
- [ ] **Secrets Management:** Ensure there are NO plaintext database passwords in the ECS task definition environment variables or the ECR image. Use AWS Secrets Manager and reference it via the `secrets[]` array in the task definition.
- [ ] **ECR Image:** Ensure the private ECR repository `catalog-service` exists and contains an image tagged as `catalog-service:1.0.0`.

---

## 4. Reliability
- [ ] **ECS Auto Scaling Limits:** Set the Application Auto Scaling scalable target with `MinCapacity=2` and `MaxCapacity=15`.
- [ ] **ECS Scaling Policy:** Use target tracking based on the `ALBRequestCountPerTarget` metric with a `TargetValue=200`.
- [ ] **ECS Scaling Cooldowns:** Set the scale-out cooldown to `30 seconds` and the scale-in cooldown to `300 seconds`.
- [ ] **ALB Target Group:** Set the deregistration delay timeout on `titanflow-<state>-tg` to exactly `30 seconds`.
- [ ] **DynamoDB GSI (Category):** Create `CategoryIndex` (PK=`category` [String], SK=`product_id` [String], Projection=`ALL`).
- [ ] **DynamoDB GSI (Warehouse):** Create `WarehouseIndex` (PK=`warehouse_zone` [String], SK=`last_updated` [String], Projection=`ALL`).
- [ ] **DynamoDB Streams:** Enable streams on `titanflow-repo-table` with the view type `NEW_AND_OLD_IMAGES`.
- [ ] **EventBridge Pipes:** Create a pipe (`titanflow-<state>-pipe`) reading from the DynamoDB Stream. Ensure it is `RUNNING` and has a filter criteria that only matches `INSERT` events.
- [ ] **DynamoDB PITR:** Enable Point-in-Time Recovery on the `titanflow-repo-table`.

---

## 5. Performance Efficiency
- [ ] **API Gateway Caching Configuration:** Enable caching on the `prod` stage with a `0.5 GB` capacity and a default TTL of `180 seconds`.
- [ ] **Cache Overrides:** Configure method-level caching so that `GET /products/{id}` is cached, but `POST /products` and list-style query routes are explicitly *uncached*.
- [ ] **ALB Health Checks:** Set the health check path to `/health`, the healthy threshold to `2`, and the interval to `15 seconds`.
- [ ] **Container Health Checks:** Ensure the container definition has a health check command that validates the local `/health` endpoint (e.g., using `wget`).
- [ ] **High Availability:** Ensure ECS service tasks are distributed across at least 2 distinct Availability Zones.
- [ ] **SQS Configuration:** Set the `VisibilityTimeout` of `titanflow-<state>-inventory-queue` to `30 seconds`.
- [ ] **Live Score:** Ensure your API is performant and actively receiving traffic to rank highly on the leaderboard before the competition closes.

---

## 6. Sustainability
- [ ] **Log Retention (ECS):** Set the CloudWatch log group `/ecs/catalog-service` retention policy to `30 days` or fewer.
- [ ] **Log Retention (VPC):** Set the CloudWatch log group `titanflow-<state>-flowlogs` retention policy to `30 days` or fewer.
- [ ] **SQS Dead Letter Queue (DLQ):** Ensure `titanflow-<state>-inventory-dlq` exists and is configured as the redrive target for the main inventory queue so failed messages do not sit in the main queue invisibly.

---

## 7. Work Organization and Management
- [ ] **Naming Conventions:** Strictly follow the `titanflow-<state>-<suffix>` naming convention for ALL created resources (Cluster, Service, ALB, Target Group, API GW, WAF, SQS Queues, EventBridge Pipe, Backup Vault, Log Groups, SNS Alerts, Dashboard).
- [ ] **Tagging:** Apply the `CompetitorId=<state_code>` tag to all resources. (Grading checks that at least 5 distinct resource types have this tag).
- [ ] **SSM Parameters:** Update the Systems Manager Parameter Store value `/titanflow/api_endpoint` with your valid HTTPS API Gateway invoke URL (it must end with `/prod`).
- [ ] **AWS Backup Setup:** Create a backup vault named `titanflow-<state>-vault` and a backup plan named `titanflow-<state>-backup`. Assign the `titanflow-repo-table` DynamoDB table as a protected resource in this plan.
