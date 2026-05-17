# Amazon EFS (Elastic File System)

Amazon EFS provides a simple, scalable, fully managed elastic NFS file system for use with AWS Cloud services and on-premises resources.

## 1. Distributed Storage Architecture

### Posix-Compliant Shared File Systems
Designed for Linux-based workloads. EFS provides standard file system semantics, allowing thousands of EC2 instances to connect and share data concurrently.

### Mount Targets and VPC Placement
To access EFS from your VPC, you create Mount Targets in your subnets. You secure these mount targets using Security Groups to dictate which instances can mount the file system.

### EFS Storage Classes
- **Standard / One Zone**: Standard stores data redundantly across multiple AZs. One Zone stores data in a single AZ at a lower cost.
- **Infrequent Access (IA) / Archive**: Lower-cost tiers for data that is accessed less frequently (IA) or rarely (Archive).

### Lifecycle Management
Automates the tiering of files. For example, files not accessed for 30 days are automatically transitioned from Standard to the Infrequent Access or Archive tiers, optimizing costs without changing the file system namespace.

## 2. Performance & Throughput Modes

### Elastic Throughput Mode vs. Provisioned Throughput Mode
- **Elastic Throughput**: Automatically scales throughput performance up or down based on your workload's needs. You pay only for the data read/written.
- **Provisioned Throughput**: You explicitly define the throughput (MB/s) of the file system, independent of the amount of data stored.

### General Purpose Performance Mode vs. Max I/O Performance Mode
- **General Purpose**: The default mode, ideal for latency-sensitive use cases (web serving, CMS).
- **Max I/O**: Optimized for applications where tens, hundreds, or thousands of EC2 instances access the file system simultaneously (Big Data, HPC), sacrificing a bit of per-operation latency for massive aggregate throughput.
