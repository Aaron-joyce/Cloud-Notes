# Amazon CloudWatch

Amazon CloudWatch is the primary native hub for monitoring infrastructure, platform, and application performance on AWS.

## Core Observability Features

### CloudWatch Logs
Collects, monitors, and stores log files from EC2, Lambda, ECS, and custom sources. It features **Logs Insights**, a purpose-built query language for fast interactive JSON parsing and log querying.

### CloudWatch Metrics
Ingests and aggregates real-time performance data points. It supports **Metric Math** (performing calculations across multiple metrics) and **Anomaly Detection** to dynamically adjust alarm baselines based on historical trends instead of static thresholds.

### CloudWatch Application Signals
The native Application Performance Monitoring (APM) layer that auto-instruments workloads (like Java/NodeJS code on EKS or ECS). It automatically builds application topologies, service maps, and tracks Service Level Objectives (SLOs).

## Evidentiary & End-User Experience

### CloudWatch RUM (Real User Monitoring)
Collects client-side telemetry (such as page load times, JavaScript errors, and user behavior) directly from actual web application user sessions.

### CloudWatch Synthetics
Runs configurable, scheduled scripts known as "canaries" to mimic user behavior. These canaries ping modular endpoints or APIs 24/7 to continuously verify availability and latency.

### Container Insights & Lambda Insights
Pre-configured monitoring infrastructure specialized for collecting deep, enhanced diagnostic telemetry from containerized clusters (EKS/ECS) and serverless environments (Lambda).

## Operational AI & Root Cause Analysis

CloudWatch includes advanced AIOps features designed to help platform teams isolate complex failures across highly distributed systems using machine learning.

### CloudWatch Investigations
An automated diagnostic framework that correlates firing alarms, anomalies, and active deployments to deliver natural language root-cause analysis summaries.

### CloudWatch Logs Anomaly Detection
Automatically scans high-volume logging clusters to categorize log structures and immediately flag structural anomalies or unexpected spikes in application errors.

### Model & Agent Observability
Provides native integration hooks built to continuously track the input/output latency, token consumption, and systemic errors of generative AI systems running inside Amazon Bedrock AgentCore.
