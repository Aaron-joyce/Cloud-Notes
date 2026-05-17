Migration Guide: RDS to DynamoDB (Manual ETL)
This document outlines the process, architecture, and implementation details for migrating data from a relational database (RDS) to a NoSQL key-value store (DynamoDB) without using AWS DMS.
1. Architecture Overview
Since RDS is a structured, relational engine and DynamoDB is a schema-less, non-relational engine, a direct "copy-paste" is not possible. The process follows a custom ETL (Extract, Transform, Load) pattern.
 * Extract: Querying data from RDS (SQL).
 * Transform: Mapping relational rows to DynamoDB JSON items (Denormalization).
 * Load: Writing data using the DynamoDB BatchWriteItem API.
2. Key Differences & Modeling
Before migrating, you must redefine your data structure:
| Feature | RDS (SQL) | DynamoDB (NoSQL) |
|---|---|---|
| Schema | Rigid/Fixed | Flexible/Schema-less |
| Relationships | Joins (Foreign Keys) | Denormalized (Single Table Design) |
| Primary Key | Usually Auto-increment ID | Partition Key + Sort Key |
| Scaling | Vertical (Larger Instance) | Horizontal (Partitioning) |
Single Table Design Strategy
In DynamoDB, avoid creating one table for every SQL table. Instead, use generic attributes like PK (Partition Key) and SK (Sort Key) to store multiple entity types in one table.
3. Migration Implementation (Python/Boto3)
The following script handles the extraction from a PostgreSQL/MySQL RDS instance and performs a batch load into DynamoDB.
import boto3
import psycopg2 # Use mysql.connector for MySQL
from botocore.exceptions import ClientError
import time
from decimal import Decimal

# --- Configuration ---
RDS_CONFIG = {
    'dbname': 'inventory_db',
    'user': 'admin',
    'password': 'yourpassword',
    'host': 'rds-instance-endpoint.amazonaws.com'
}

DYNAMO_TABLE_NAME = 'MigratedAssets'
BATCH_SIZE = 25  # DynamoDB maximum batch size

# Initialize AWS Resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def transform_to_dynamo(row):
    """
    Transforms a SQL row tuple into a DynamoDB dictionary.
    Handles Data Type conversions (e.g., Decimals, Strings).
    """
    return {
        'PK': f"ORG#{row[0]}",          # Organization ID
        'SK': f"USER#{row[1]}",         # User ID
        'Email': str(row[2]),
        'AccountBalance': Decimal(str(row[3])), # Convert float to Decimal
        'LastLogin': str(row[4]),       # ISO-8601 String
        'IsActive': bool(row[5])
    }

def run_migration():
    # 1. Connect to RDS
    try:
        conn = psycopg2.connect(**RDS_CONFIG)
        cur = conn.cursor()
        print("Connected to RDS...")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Extract Data
    cur.execute("SELECT org_id, user_id, email, balance, last_login, active FROM users")
    
    batch = []
    total_count = 0

    # 3. Process and Load
    while True:
        row = cur.fetchone()
        if row is None:
            if batch: # Finalize last batch
                send_batch(batch)
            break

        item = transform_to_dynamo(row)
        batch.append({'PutRequest': {'Item': item}})
        total_count += 1

        if len(batch) == BATCH_SIZE:
            send_batch(batch)
            batch = []
            print(f"Migrated {total_count} items...")

    cur.close()
    conn.close()
    print("Migration finished successfully.")

def send_batch(batch_items):
    """
    Uses batch_write_item to push data efficiently.
    Includes logic to handle UnprocessedItems (Throttling).
    """
    try:
        response = dynamodb.meta.client.batch_write_item(
            RequestItems={DYNAMO_TABLE_NAME: batch_items}
        )
        
        # Handle Throttling/Provisioned Throughput errors
        unprocessed = response.get('UnprocessedItems', {})
        while unprocessed:
            print("Retrying unprocessed items...")
            time.sleep(2) # Exponential backoff
            response = dynamodb.meta.client.batch_write_item(RequestItems=unprocessed)
            unprocessed = response.get('UnprocessedItems', {})
            
    except ClientError as e:
        print(f"Client Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    run_migration()

4. Best Practices for Large Migrations
Capacity Management
 * Switch to On-Demand: Set your DynamoDB table to PAY_PER_REQUEST during the migration to avoid 400 errors.
 * Provisioned Mode: If using Provisioned mode, increase Write Capacity Units (WCU) significantly before starting, then scale down after completion.
Data Consistency (The Dual-Write Phase)
Since this is a manual migration, there is no automatic sync for new data coming into RDS during the script execution.
 * Phase 1: Run the Bulk Migration script for historical data.
 * Phase 2: Update your Application Logic to write to both RDS and DynamoDB for all new transactions.
 * Phase 3: Verify data integrity and decommission the RDS writes.
Error Handling
 * Decimals: DynamoDB requires the Decimal type for numbers with precision; standard Python floats will throw errors.
 * Timeouts: For massive RDS tables, use Server-Side Cursors (in psycopg2, this is done by naming the cursor: conn.cursor('cursor_name')) to avoid loading the entire dataset into the script's memory.
 * 
