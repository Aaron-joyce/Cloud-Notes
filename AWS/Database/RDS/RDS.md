# Amazon RDS (Relational Database Service)

Amazon Relational Database Service (RDS) is a managed distributed relational database service by Amazon Web Services.

## 1. Database Engines & Architecture

### Supported Engines
RDS supports multiple database engines: Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle, and Microsoft SQL Server.

### Multi-AZ Deployments
Features synchronous replication to a standby instance in a different Availability Zone (AZ) for high availability and automatic failover in case of infrastructure failure.

### Read Replicas
Allows for asynchronous replication of the primary database to one or more read replicas. This is used to scale out read-heavy workloads and can also be promoted to a standalone database if needed.

### Amazon Aurora Architecture
Aurora is a fully managed, MySQL- and PostgreSQL-compatible relational database built for the cloud. It features a shared, auto-scaling storage volume that is distributed and replicated across 3 Availability Zones (6 copies of data).

## 2. Maintenance, Backups, and Recovery

### Automated Backups & Backup Windows
RDS performs automated backups of your database instances during a specified backup window. Transaction logs are retained alongside these backups, enabling Point-in-Time Recovery (PITR) to restore to any second during the retention period.

### Manual Snapshots
Persistent, user-initiated storage states preserved even after the original database instance is deleted.

### Automated Patching & Maintenance Windows
RDS allows you to specify a maintenance window during which OS and database engine patching occurs automatically.

### Storage Auto-Scaling
Dynamically extends disk capacity as your database grows, without application downtime, preventing out-of-storage errors.

## 3. Security & Networking

### VPC Isolation & DB Subnet Groups
RDS instances are launched within an Amazon VPC. DB Subnet Groups define which subnets (and thus AZs) the database can be provisioned in, typically private subnets for security.

### IAM Database Authentication vs. Native Credentials
You can authenticate to MySQL and PostgreSQL using AWS IAM users and roles instead of relying solely on native database usernames and passwords.

### Transparent Data Encryption (TDE) and AWS KMS
RDS supports encryption at rest using AWS KMS keys. Oracle and SQL Server support Transparent Data Encryption (TDE).

### Secure Socket Layer (SSL/TLS)
RDS enforces and supports SSL/TLS to encrypt data in transit between your application and the database instance.
