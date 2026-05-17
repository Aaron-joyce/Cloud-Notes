# AWS Elastic Compute Cloud (EC2) Overview

## What is Amazon EC2?
Amazon Elastic Compute Cloud (Amazon EC2) provides scalable computing capacity in the Amazon Web Services (AWS) Cloud. Using Amazon EC2 eliminates your need to invest in hardware up front, so you can develop and deploy applications faster. You can use Amazon EC2 to launch as many or as few virtual servers as you need, configure security and networking, and manage storage.

---

## Related Services in the EC2 Console
The EC2 Dashboard in the AWS Management Console groups several related services and features that are essential for managing compute resources. Here is an overview:

### Compute
- **EC2 Instances**: The core virtual servers you run your applications on.
- **Dedicated Hosts**: Physical servers with EC2 instance capacity fully dedicated to your use, which can help you address compliance requirements and reduce costs by using your existing server-bound software licenses.
- **Spot Requests**: Allows you to request unused EC2 instances at steep discounts, suitable for fault-tolerant and flexible applications.

### Network & Security
- **Security Groups**: Act as a virtual firewall for your EC2 instances to control incoming and outgoing traffic at the instance level.
- **Elastic IPs**: Static IPv4 addresses designed for dynamic cloud computing. An Elastic IP address is allocated to your AWS account, and is yours until you release it.
- **Placement Groups**: Determine how instances are placed on underlying hardware (Cluster, Spread, Partition) to meet specific needs like low latency or high availability.
- **Key Pairs**: Secure login information for your instances. AWS stores the public key, and you store the private key.
- **Network Interfaces (ENI)**: A logical networking component in a VPC that represents a virtual network card.

### Load Balancing & Auto Scaling
- **Load Balancers**: Automatically distributes incoming application traffic across multiple targets, such as Amazon EC2 instances, containers, IP addresses, and Lambda functions. (ALB, NLB, GLB)
- **Target Groups**: Used to route requests from a load balancer to one or more registered targets.
- **Auto Scaling Groups**: Contains a collection of Amazon EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management.
- **Launch Templates / Configurations**: Define the parameters to launch EC2 instances within an Auto Scaling group or independently. Launch Templates are the newer, recommended approach.

### Storage (Elastic Block Store)
- **Volumes**: Persistent block storage volumes for use with EC2 instances. Can be HDD or SSD based.
- **Snapshots**: Point-in-time backups of EBS volumes stored in Amazon S3.
- **Lifecycle Manager**: Automates the creation, retention, and deletion of EBS snapshots and EBS-backed AMIs.

### Images
- **AMIs (Amazon Machine Images)**: Provides the information required to launch an instance. An AMI includes the operating system, application server, and applications. You can use AWS-provided AMIs, community AMIs, AWS Marketplace AMIs, or create your own custom AMIs.

---

## In-Depth: EC2 Instances

### 1. Instance Types
EC2 provides a wide selection of instance types optimized to fit different use cases. Instance types comprise varying combinations of CPU, memory, storage, and networking capacity.

- **General Purpose (e.g., T, M series)**: Provide a balance of compute, memory, and networking resources. Ideal for web servers, development environments, and code repositories.
- **Compute Optimized (e.g., C series)**: Ideal for compute-bound applications that benefit from high-performance processors (e.g., batch processing, media transcoding, high-performance web servers, machine learning inference).
- **Memory Optimized (e.g., R, X series)**: Designed to deliver fast performance for workloads that process large data sets in memory (e.g., high-performance databases, distributed web scale in-memory caches).
- **Accelerated Computing (e.g., P, G series)**: Use hardware accelerators, or co-processors (GPUs, FPGAs), to perform functions such as floating-point number calculations, graphics processing, or data pattern matching more efficiently than is possible in software running on CPUs.
- **Storage Optimized (e.g., I, D series)**: Designed for workloads that require high, sequential read and write access to very large data sets on local storage (e.g., NoSQL databases, in-memory databases, data warehousing).

### 2. Instance Purchasing Options (Pricing Models)
You can purchase EC2 instances in several different ways based on your application's needs and budget:

- **On-Demand Instances**: Pay for compute capacity by the second with no long-term commitments. Good for unpredictable workloads, testing, and short-term applications.
- **Reserved Instances (RIs)**: Provide a significant discount (up to 72%) compared to On-Demand pricing. You commit to a 1- or 3-year term. Good for steady-state usage.
- **Savings Plans**: A flexible pricing model that offers lower prices compared to On-Demand pricing, in exchange for a specific usage commitment (measured in $/hour) for a 1- or 3-year period.
- **Spot Instances**: Request spare Amazon EC2 computing capacity for up to 90% off the On-Demand price. These can be interrupted by AWS with a 2-minute warning. Ideal for fault-tolerant, flexible workloads, batch jobs, and background processing.
- **Dedicated Hosts**: A physical EC2 server dedicated for your use. Useful for bringing your own software licenses (BYOL) to the cloud and meeting regulatory compliance.
- **Dedicated Instances**: Instances that run in a virtual private cloud (VPC) on hardware that's dedicated to a single customer.

### 3. Instance Lifecycle
An EC2 instance transitions through several states from the moment it is launched to when it is terminated.

* **Pending**: The instance is preparing to enter the `running` state. AWS is allocating compute resources.
* **Running**: The instance is running and ready for use. You incur charges in this state.
* **Stopping**: The instance is shutting down. (Only available for EBS-backed instances).
* **Stopped**: The instance is shut down and not incurring EC2 charges (EBS storage charges still apply). You can start it again.
* **Shutting-down**: The instance is preparing to be terminated.
* **Terminated**: The instance has been permanently deleted and cannot be started again. Ephemeral storage and, by default, the root EBS volume are deleted.

### 4. Root Device Storage
Every instance has a root volume that contains the image used to boot the instance.
- **EBS-Backed Instances**: The root device is an Amazon EBS volume. These instances can be stopped and started. Data persists when stopped.
- **Instance Store-Backed Instances**: The root device is an instance store volume created from a template stored in Amazon S3. These volumes are ephemeral; if the instance is stopped, terminated, or if the underlying drive fails, data is lost.

### 5. Instance User Data & Metadata
- **User Data**: When you launch an instance, you can pass user data to it. This is typically used to perform common automated configuration tasks and run scripts after the instance starts (e.g., installing a web server, downloading code).
- **Metadata**: Instance metadata is data about your instance that you can use to configure or manage the running instance. It can be accessed from within the instance itself via an HTTP request to a special IP address (e.g., `curl http://169.254.169.254/latest/meta-data/`). This provides information like the instance ID, private IP, public IP, and attached IAM role credentials.
