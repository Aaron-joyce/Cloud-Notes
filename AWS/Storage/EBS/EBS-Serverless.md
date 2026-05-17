# Amazon EBS (Elastic Block Store)

Amazon EBS provides highly available, consistent, low-latency block storage volumes for use with Amazon EC2 instances.

## 1. Volume Types & Performance Characteristics

### Solid State Drives (SSD)
Designed for transactional, IOPS-intensive workloads (boot volumes, databases).
- **General Purpose (gp2, gp3)**: Balances price and performance. gp3 allows provisioning IOPS and throughput independently of volume size.
- **Provisioned IOPS (io2, io2 Block Express)**: Designed for I/O-intensive database workloads requiring sustained, high-performance IOPS.

### Hard Disk Drives (HDD)
Designed for large, sequential, throughput-intensive workloads (Big Data, data warehouses). Cannot be used as boot volumes.
- **Throughput Optimized (st1)**: For frequently accessed, throughput-intensive workloads.
- **Cold HDD (sc1)**: Lowest cost storage for infrequently accessed workloads.

### Performance Metrics
- **IOPS**: Input/Output Operations Per Second. Crucial for databases and random read/write workloads.
- **Throughput**: Measured in MB/s. Crucial for large sequential data transfers like media streaming or analytics.
- **Latency boundaries**: The time it takes for an I/O operation to complete.

### EBS Burst Balance and Baseline Performance
Volumes like gp2 have a baseline performance tied to their size and accumulate "I/O credits" when idle, which can be spent to burst performance during spikes. gp3 simplifies this by providing a predictable baseline without burst credits.

## 2. Advanced Lifecycle & Architecture Primitives

### EBS Snapshots & Data Lifecycle Manager (DLM)
- **Snapshots**: Point-in-time, incremental backups of EBS volumes stored in Amazon S3.
- **DLM**: A service that automates the creation, retention, and deletion of EBS snapshots based on defined schedules and tags.

### Fast Snapshot Restore (FSR)
Eliminates the volume initialization (warming) latency typically associated with creating a volume from a snapshot. FSR ensures that the newly created volume delivers its maximum provisioned performance immediately.

### Elastic Volumes
Allows you to dynamically increase capacity, tune performance (IOPS/throughput), or change the volume type on-the-fly without detaching the volume or experiencing application downtime.

### EBS Multi-Attach
Allows you to attach a single Provisioned IOPS (io1/io2) volume concurrently to multiple Nitro-based EC2 instances within the same Availability Zone. Essential for clustered applications that manage concurrent write operations.
