# Building a Highly Available, Self-Healing Web Architecture on AWS

This guide provides a comprehensive, step-by-step walkthrough to build a highly available (HA), self-healing, and scalable web server architecture using Amazon EC2, Application Load Balancers (ALB), and Auto Scaling Groups (ASG).

## Architectural Overview
* **High Availability (HA):** Traffic is distributed across instances in at least two different Availability Zones (AZs) using an ALB. If one AZ experiences an outage, the application remains available in the other.
* **Self-Healing:** The ASG is configured to rely on ELB health checks. If an application crashes (even if the underlying EC2 hardware is fine), the load balancer marks the instance as unhealthy. The ASG then automatically terminates the bad instance and spins up a fresh replacement.
* **Scalability:** The ASG dynamically adjusts the number of running instances based on CPU utilization to handle traffic spikes and save costs during low traffic.

---

## Prerequisites
Before starting, ensure you have:
* A Default VPC (or a custom VPC) with an Internet Gateway attached.
* At least **two public subnets** in two different Availability Zones (e.g., `us-east-1a` and `us-east-1b`).

---

## Step 1: Configure Security Groups
Proper security group configuration is crucial. The EC2 instances should only accept traffic from the Load Balancer, not directly from the internet.

1. **Create the ALB Security Group (`alb-sg`):**
   * **Inbound Rules:** Allow HTTP (Port 80) and HTTPS (Port 443) from `0.0.0.0/0` (Anywhere).
   * **Outbound Rules:** Allow all traffic to `0.0.0.0/0`.
2. **Create the EC2 Web Server Security Group (`web-sg`):**
   * **Inbound Rules:** Allow HTTP (Port 80) **only from the `alb-sg`**. (Under "Source", select "Custom" and search for the security group ID of `alb-sg`). Allow SSH (Port 22) from your IP if you need terminal access.
   * **Outbound Rules:** Allow all traffic to `0.0.0.0/0`.

---

## Step 2: Create a Launch Template
The launch template defines how the ASG will spin up new web servers.

1. Navigate to **EC2 Dashboard -> Launch Templates** and click **Create launch template**.
2. Name it `HA-Web-Template`.
3. **AMI:** Choose Amazon Linux 2023 (or Amazon Linux 2).
4. **Instance Type:** Choose `t2.micro` or `t3.micro` (Free Tier eligible).
5. **Key pair:** Select an existing key pair or create a new one.
6. **Network Settings:** 
   * Do NOT specify a subnet here (the ASG handles this).
   * **Security groups:** Select the `web-sg` created in Step 1.
7. **Advanced Details (User Data):** 
   Scroll to the bottom to the "User data" field. This script installs and starts an Apache web server automatically upon boot:
   ```bash
   #!/bin/bash
   yum update -y
   yum install -y httpd
   systemctl start httpd
   systemctl enable httpd
   echo "<h1>Hello from HA Web Server running in $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</h1>" > /var/www/html/index.html
   ```
8. Click **Create launch template**.

---

## Step 3: Create the Application Load Balancer (ALB)
The ALB will be the single point of contact for clients.

1. Navigate to **EC2 Dashboard -> Target Groups** and click **Create target group**.
   * **Target type:** Instances.
   * **Target group name:** `web-tg`.
   * **Protocol / Port:** HTTP / 80.
   * **VPC:** Select your VPC.
   * **Health checks:** Path `/`, keeping the default settings.
   * Click Next, do *not* register any targets manually, and click **Create target group**.
2. Navigate to **EC2 Dashboard -> Load Balancers** and click **Create Load Balancer**.
3. Choose **Application Load Balancer**.
4. **Name:** `HA-Web-ALB`.
5. **Scheme:** Internet-facing.
6. **Network mapping:** Select your VPC and check at least **two Availability Zones** and their corresponding public subnets.
7. **Security groups:** Remove the default SG and select the `alb-sg` created in Step 1.
8. **Listeners and routing:** For the HTTP:80 listener, select **Forward to** and choose the `web-tg` target group.
9. Click **Create load balancer**.

---

## Step 4: Create the Auto Scaling Group (ASG)
This is where we tie the template and the load balancer together and enable self-healing.

1. Navigate to **EC2 Dashboard -> Auto Scaling Groups** and click **Create Auto Scaling group**.
2. **Name:** `HA-Web-ASG`.
3. **Launch template:** Select `HA-Web-Template` and click Next.
4. **Network:** Select your VPC. Under **Availability Zones and subnets**, select the *same public subnets* you mapped to your ALB in Step 3. Click Next.
5. **Advanced Options (Crucial for Self-Healing):**
   * Under **Load balancing**, choose **Attach to an existing load balancer**.
   * Choose **Choose from your load balancer target groups** and select `web-tg`.
   * Under **Health checks**, check the box for **Turn on Elastic Load Balancing health checks**. 
     *(Why? If an EC2 instance is running but the Apache service crashes, EC2 thinks the instance is healthy. However, the ALB will fail its HTTP health check. By enabling this, the ASG listens to the ALB and will replace the instance if Apache crashes).*
6. **Group Size and Scaling Policies:**
   * **Desired capacity:** 2
   * **Minimum capacity:** 2
   * **Maximum capacity:** 4
   * Under **Scaling policies**, choose **Target tracking scaling policy**.
   * **Metric type:** Average CPU utilization.
   * **Target value:** `50` (The ASG will launch more instances if the average CPU across the fleet exceeds 50%).
7. Skip Notifications and Tags, or configure as desired.
8. Click **Create Auto Scaling group**.

---

## Step 5: Verification & Testing

### 1. Verify High Availability
1. Go to your Load Balancers, select `HA-Web-ALB`, and copy its **DNS name** (e.g., `HA-Web-ALB-1234.us-east-1.elb.amazonaws.com`).
2. Paste the DNS name into your browser. You should see the message: `Hello from HA Web Server running in us-east-1a`.
3. Refresh the page a few times. You should eventually see the AZ change (e.g., `us-east-1b`), proving the ALB is routing traffic across both AZs.

### 2. Test Self-Healing
1. Go to the **Instances** dashboard. You should see two instances running, spun up by the ASG.
2. Select one of the instances and explicitly **Terminate** it.
3. Refresh the Instances dashboard. Almost immediately, you will see the terminated instance shutting down, and a brand **new instance** in a `Pending` state. The ASG noticed the desired capacity dropped from 2 to 1 and instantly self-healed the fleet.

### 3. Test Scaling (Optional)
To test scaling out, SSH into one of the instances and run a stress test command to artificially spike the CPU to 100%:
```bash
sudo amazon-linux-extras install epel -y
sudo yum install stress -y
stress -c 4
```
Wait a few minutes. Check the Auto Scaling Group's "Activity" tab; you will see it automatically launching new instances to handle the CPU load, bringing the total count up to your maximum capacity. Once you terminate the stress command, it will eventually scale back in.
