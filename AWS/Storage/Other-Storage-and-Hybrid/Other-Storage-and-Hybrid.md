# Other AWS Storage & Hybrid Cloud Solutions

## 1. AWS Storage Gateway (Hybrid Cloud Integration)

AWS Storage Gateway is a hybrid cloud storage service that gives you on-premises access to virtually unlimited cloud storage.

### Amazon S3 File Gateway
Bridges on-premises applications to Amazon S3. It presents a file interface (using SMB or NFS protocols) to your local networks, asynchronously uploading files to S3 as objects while maintaining a local cache of recently accessed data for low-latency retrieval.

### Amazon FSx File Gateway
Provides fast, local, low-latency cache access for remote on-premises clients connecting to cloud-based Amazon FSx for Windows File Server file shares over SMB.

### Volume Gateway
Exposes cloud-backed iSCSI block storage volumes to your local on-premises applications.
- **Cached Mode**: Stores primary data in S3, retaining a local cache of frequently accessed data.
- **Stored Mode**: Stores all data locally for low latency, asynchronously backing it up to S3 as EBS snapshots.

### Tape Gateway
Replaces physical tape backup workflows with virtual tape libraries (VTL). It integrates with existing backup software (like Veeam or Backup Exec) and stores virtual tapes durably in Amazon S3 and S3 Glacier.

## 2. AWS Snow Family (Edge & Offline Data Migration)

The AWS Snow Family consists of physical devices used to physically transport petabytes of data into and out of AWS, bypassing network constraints.

### AWS Snowcone
An ultra-portable, ruggedized, secure device for small data migrations (up to 8 TB) and lightweight edge computing workloads. It can be shipped via mail.

### AWS Snowball Edge
A petabyte-scale physical storage and compute device used in disconnected environments (like ships or remote factories).
- **Storage Optimized**: Focused on large-scale data migration.
- **Compute Optimized**: Includes powerful compute resources and optional GPUs for advanced edge processing or machine learning before data is moved to the cloud.

### AWS DataSync
An online data transfer service that automates, schedules, and accelerates moving data between on-premises storage systems (NFS, SMB) and AWS storage services (S3, EFS, FSx) over the network, handling validation and encryption automatically.
