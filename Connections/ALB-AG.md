Here is a detailed Markdown guide you can save as a `.md` file for your project documentation. It covers both the public "Quick Start" method and the private "Production-Ready" method.

---

# AWS API Gateway to ALB Integration Guide

This document outlines the steps to connect an **AWS API Gateway (REST API)** to an **Application Load Balancer (ALB)** powering an **ECS Fargate** backend.

---

## Method 1: Public ALB (HTTP Proxy)
*Use this for rapid prototyping or simple school projects where the ALB is already accessible via the internet.*

### 1. Prerequisites
* A Public ALB with a functional Target Group pointing to your ECS Fargate tasks.
* The DNS Name of your ALB (e.g., `my-alb-123.us-east-1.elb.amazonaws.com`).
* **Security Group Check:** Ensure the ALB's Security Group allows **Inbound HTTP (Port 80)** from `0.0.0.0/0`.

### 2. API Gateway Configuration
1. Open the **API Gateway Console** and select your REST API.
2. Create a **Resource**:
   * Click **Create Resource**.
   * Toggle **Proxy Resource** to ON.
   * Resource Path: `/`
   * Resource Name: `{proxy+}`
3. Create the **Method**:
   * For **Integration type**, select **HTTP**.
   * Check **Use HTTP Proxy integration**.
   * **HTTP method**: `ANY`.
   * **Endpoint URL**: `http://YOUR-ALB-DNS-NAME/{proxy}`
4. **Deploy**:
   * Click **Deploy API**.
   * Select or create a stage (e.g., `prod`).
   * Your API is now live at the Invoke URL.

---

## Method 2: Private ALB (VPC Link)
*Use this for production environments to ensure your backend is not exposed to the public internet.*

### 1. Prerequisites
* An **Internal ALB** (Scheme: internal) sitting in your Private Subnets.
* The Private DNS Name of your ALB.
* **Security Group Check:** The ALB must allow inbound traffic from the VPC Link's security group (created in the next step).

### 2. Create the VPC Link (v2)
1. In the API Gateway sidebar, click **VPC Links**.
2. Click **Create** and choose **VPC link for REST APIs**.
3. Configure the following:
   * **Name**: `alb-vpc-link`
   * **VPC**: Select the VPC where your ALB resides.
   * **Subnets**: Select at least two private subnets.
   * **Security Groups**: Create or select a security group for the link itself.

### 3. Configure API Integration
1. Go to your API **Resources** and select the `{proxy+}` method.
2. Set **Integration type** to **VPC Link**.
3. Check **Use Proxy Integration**.
4. **VPC Link**: Select the link you created in Step 2.
5. **Endpoint URL**: `http://YOUR-INTERNAL-ALB-DNS/{proxy}`
   * *Note: Use `http` or `https` depending on your ALB listener settings.*

### 4. Final Security Check
* Navigate to your **ALB Security Group**.
* Add an **Inbound Rule**:
  * **Type**: HTTP (80)
  * **Source**: The **Security Group ID** assigned to your **VPC Link**.

---

## Troubleshooting Common Errors

| Error Code | Likely Cause | Solution |
| :--- | :--- | :--- |
| **502 Bad Gateway** | Target Group issues or Header mismatch. | Ensure your ECS task is healthy in the Target Group. |
| **504 Gateway Timeout** | Security Group blocking traffic. | Check that the ALB allows traffic from API Gateway (Method 1) or VPC Link (Method 2). |
| **403 Forbidden** | IAM or WAF restrictions. | Ensure you don't have a Resource Policy on the API Gateway blocking access. |

---

Would you like me to add a section on how to handle SSL/HTTPS termination between the Gateway and the ALB?