# Amazon EBS (Elastic Block Store)

Amazon EBS provides highly available, persistent block storage volumes for use with Amazon EC2 instances.

## 1. Volume Types & Performance Characteristics

### Solid State Drives (SSD)
- **General Purpose (gp2, gp3)**: Cost-effective storage for a broad range of workloads. `gp3` allows provisioning IOPS and throughput independently of volume size.
- **Provisioned IOPS (io2, io2 Block Express)**: High-performance volumes designed for mission-critical, latency-sensitive databases.

### Hard Disk Drives (HDD)
- **Throughput Optimized (st1)**: Low-cost magnetic storage designed for large, sequential workloads like big data, data warehouses, and log processing.
- **Cold HDD (sc1)**: Lowest-cost magnetic storage for infrequently accessed sequential workloads.

### Performance Metrics
- **IOPS**: Input/Output Operations Per Second. Crucial for random read/write workloads (like databases).
- **Throughput (MB/s)**: The rate at which data is transferred. Crucial for large sequential workloads.
- **Latency**: The time it takes for an I/O operation to complete.

### EBS Burst Balance and Baseline Performance models
Smaller `gp2` volumes have a baseline IOPS performance and earn "burst credits". When demand spikes, they consume burst credits to achieve higher IOPS. `gp3` provides a consistent baseline of 3,000 IOPS regardless of size.

## 2. Advanced Lifecycle & Architecture Primitives

### EBS Snapshots & Data Lifecycle Manager (DLM)
- **Snapshots**: Point-in-time backups of EBS volumes stored incrementally in Amazon S3.
- **Data Lifecycle Manager (DLM)**: Automates the creation, retention, and deletion of EBS snapshots.

### Fast Snapshot Restore (FSR)
Eliminates the latency of volume initialization (the penalty of pulling data from S3 when first accessing blocks on a volume created from a snapshot). FSR ensures volumes are fully performant immediately upon creation.

### Elastic Volumes
Allows you to dynamically increase capacity, tune performance (IOPS/Throughput), or change the volume type of a live EBS volume on-the-fly without detaching the volume or restarting the instance.

### EBS Multi-Attach
Enables attaching a single Provisioned IOPS (`io1`/`io2`) volume concurrently to multiple Nitro-based EC2 instances within the same Availability Zone. Requires a cluster-aware file system to manage concurrent writes safely.
