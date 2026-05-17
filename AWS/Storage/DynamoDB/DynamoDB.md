# Amazon DynamoDB

Amazon DynamoDB is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale.

## 1. Data Modeling & Primary Keys

### Partition Key vs. Composite Primary Key
- **Partition Key (Hash Attribute)**: Determines the physical partition where the data is stored.
- **Composite Primary Key**: Composed of a Partition Key and a Sort Key. The Sort Key allows storing multiple items with the same partition key and sorting them logically.

### Indexes
- **Global Secondary Indexes (GSI)**: An index with a partition key and a sort key that can be different from those on the base table.
- **Local Secondary Indexes (LSI)**: An index that has the same partition key as the base table, but a different sort key. Must be created at table creation time.

### Data Types
DynamoDB supports Scalar types (String, Number, Binary, Boolean, Null), Document types (List, Map), and Set types (String Set, Number Set, Binary Set).

## 2. Throughput & Performance Optimization

### Provisioned Capacity
You explicitly define the Read Capacity Units (RCUs) and Write Capacity Units (WCUs) your application requires. Good for predictable workloads.

### On-Demand Capacity Mode
DynamoDB automatically instantly scales capacity to accommodate workloads. You pay per request. Good for unpredictable or spikey workloads.

### DynamoDB Accelerator (DAX)
A fully managed, highly available, in-memory cache for DynamoDB that delivers up to a 10x performance improvement, reducing latency from milliseconds to microseconds.

### Partition Splitting & Hot Key Mitigation
DynamoDB scales horizontally by splitting partitions as data or throughput grows. Designing proper partition keys is critical to avoid "hot keys" where traffic is unevenly distributed to a single partition.

## 3. Consistency, High Availability, and Integration

### Strongly Consistent Reads vs. Eventually Consistent Reads
By default, reads are Eventually Consistent. You can request Strongly Consistent reads, which guarantees receiving the most up-to-date data reflecting all successful earlier write operations.

### DynamoDB Streams
An ordered flow of information about changes to items in a DynamoDB table (inserts, updates, deletes). Often used to trigger AWS Lambda functions for real-time processing.

### Global Tables
Fully managed, active-active multi-region replication. It allows you to deploy multi-region database tables for globally distributed applications.

### Point-in-Time Recovery (PITR)
Continuous backups of your table data for the last 35 days, protecting against accidental write or delete operations.
