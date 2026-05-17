# Amazon EC2 Auto Scaling

## What is EC2 Auto Scaling?
Amazon EC2 Auto Scaling helps you maintain application availability and allows you to automatically add or remove EC2 instances according to conditions you define. You can use the fleet management features of EC2 Auto Scaling to maintain the health and availability of your fleet, ensuring that you are running your desired number of instances.

## How it Works
Auto Scaling relies on three core components:

1. **Auto Scaling Groups (ASG):** The core of Auto Scaling. An ASG is a collection of EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management. You define a minimum, maximum, and desired capacity for the group.
2. **Launch Templates:** A Launch Template specifies the instance configuration (AMI, instance type, key pair, security groups, block device mapping) that the ASG will use to launch new instances. *(Note: Launch Configurations are the older method and are being deprecated in favor of Launch Templates).*
3. **Scaling Policies:** These are the rules that dictate when the ASG should scale out (add instances) or scale in (remove instances). These can be triggered by CloudWatch alarms (e.g., CPU utilization > 70%).

### Key Concepts
* **Minimum Capacity:** The absolute lowest number of instances your ASG is allowed to scale down to.
* **Maximum Capacity:** The absolute highest number of instances your ASG is allowed to scale up to.
* **Desired Capacity:** The number of instances the ASG currently *wants* to be running. If an instance fails a health check, the ASG will terminate it and automatically launch a new one to maintain this desired capacity.

## Benefits of Auto Scaling
* **Better Fault Tolerance:** Auto Scaling can detect when an instance is unhealthy, terminate it, and launch an instance to replace it.
* **Better Availability:** Auto Scaling ensures that your application always has the right amount of compute capacity to handle the current traffic demand across multiple Availability Zones.
* **Better Cost Management:** Auto Scaling can dynamically adjust capacity based on demand, allowing you to save money by terminating instances when demand drops.

---

## How to Set Up EC2 Auto Scaling

### Step 1: Create a Launch Template
Before creating an ASG, you need to tell it *what* kind of instance to launch.
1. Open the EC2 Dashboard and navigate to **Launch Templates** under the **Instances** section.
2. Click **Create launch template**.
3. Provide a Name and Description.
4. Select the **Amazon Machine Image (AMI)** (e.g., Amazon Linux 2023, Ubuntu).
5. Select the **Instance type** (e.g., `t3.micro`).
6. Select a **Key pair** for SSH/RDP access.
7. Under **Network settings**, choose your existing Security Groups.
8. Configure Storage (EBS volumes) and Advanced details (like User Data for startup scripts) as needed.
9. Click **Create launch template**.

### Step 2: Create an Auto Scaling Group (ASG)
1. In the EC2 Dashboard, scroll down to **Auto Scaling** and click **Auto Scaling Groups**.
2. Click **Create Auto Scaling group**.
3. **Choose launch template or configuration:** 
   * Name your ASG.
   * Select the Launch Template you created in Step 1.
   * Click Next.
4. **Choose instance launch options:**
   * Select your VPC.
   * Select the Availability Zones and Subnets where you want your instances to launch (selecting multiple AZs ensures high availability).
   * Click Next.
5. **Configure advanced options:**
   * **Load balancing:** If you are using a Load Balancer (ALB or NLB), attach it to the ASG here. Choose "Attach to an existing load balancer" and select the Target Group associated with your load balancer.
   * **Health checks:** If using a Load Balancer, it is highly recommended to enable **ELB health checks**. This ensures the ASG replaces instances if the application running on them fails, not just if the underlying EC2 hardware fails.
   * Click Next.
6. **Configure group size and scaling policies:**
   * Set your **Desired capacity** (the initial number of instances).
   * Set your **Minimum capacity** and **Maximum capacity**.
   * **Scaling policies:** Choose how you want the group to scale.
      * *Target tracking scaling policy:* (Recommended) You pick a metric, like "Average CPU Utilization," and set a target value (e.g., 50%). AWS handles the scaling out and scaling in automatically to keep the metric near the target.
   * Click Next.
7. **Add notifications (Optional):** Set up SNS topics to receive email alerts when instances launch or terminate.
8. **Add tags (Optional):** Tag your ASG and choose to propagate tags to the instances it launches (useful for billing and management).
9. **Review and Create:** Review all settings and click **Create Auto Scaling group**.

---

## Advanced Scaling Strategies
Once your ASG is created, you can fine-tune how it scales by using different policies:
* **Dynamic Scaling:** 
  * **Target Tracking:** Maintains a specific metric target (e.g., 50% CPU utilization).
  * **Step Scaling:** Scale based on alarm thresholds with specific adjustments (e.g., add 2 instances if CPU > 80%, add 4 instances if CPU > 90%).
  * **Simple Scaling:** Triggered by a single CloudWatch alarm (largely replaced by Step Scaling).
* **Scheduled Scaling:** Scale based on a predictable schedule (e.g., increase capacity every Monday at 8:00 AM before business hours, decrease capacity Friday at 6:00 PM).
* **Predictive Scaling:** Uses machine learning to analyze historical data, predict daily and weekly traffic patterns, and proactively scale out capacity ahead of predicted demand spikes.
