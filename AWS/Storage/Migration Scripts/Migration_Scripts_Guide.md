# AWS Storage Migration Scripts Guide

This guide contains a collection of manual migration scripts written in Python and Bash to transfer data between different AWS services or regions. Each section details the purpose of the scripts and how to use them.

---

## 1. DynamoDB to RDS Migration

When migrating from DynamoDB to RDS, you can either use a Python script to scan and insert data programmatically (best for small tables or when data transformation is needed) or a Bash script to export to S3 and natively import into RDS (best for large tables).

### Python Approach (Row-by-Row Scan)
**How to use:** 
1. Ensure you have the required packages installed: `pip install boto3 psycopg2`.
2. Update the configuration variables at the bottom of the script (`DDB_TABLE`, `RDS_ENDPOINT`, `DB_NAME`, `DB_USER`, `DB_PASS`) with your credentials.
3. Run the script: `python3 dynamodb_to_rds_migration.py`.

```python
import boto3
import psycopg2 # Use psycopg2 for PostgreSQL, or pymysql for MySQL
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def migrate_dynamodb_to_rds(table_name, rds_host, db_name, db_user, db_pass):
    """
    Manually migrates data from a NoSQL DynamoDB table to a Relational RDS PostgreSQL database.
    Because DynamoDB is schema-less, you must explicitly map the JSON attributes 
    to your relational columns.
    """
    # Initialize DynamoDB Resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Connect to RDS PostgreSQL
    try:
        conn = psycopg2.connect(
            host=rds_host,
            database=db_name,
            user=db_user,
            password=db_pass
        )
        cursor = conn.cursor()
        logging.info("Successfully connected to RDS.")
    except Exception as e:
        logging.error(f"Failed to connect to RDS: {e}")
        return

    logging.info(f"Starting scan of DynamoDB table: {table_name}")
    
    # Scan the DynamoDB table
    response = table.scan()
    items = response.get('Items', [])
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))

    logging.info(f"Retrieved {len(items)} items from DynamoDB. Starting RDS insertion...")

    # Insert items into RDS
    insert_query = """
        INSERT INTO users (user_id, email, created_at) 
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """
    
    success_count = 0
    for item in items:
        try:
            user_id = item.get('UserId')
            email = item.get('Email', 'no-email@example.com')
            created_at = item.get('CreatedAt', '1970-01-01')
            
            cursor.execute(insert_query, (user_id, email, created_at))
            success_count += 1
            
        except Exception as e:
            logging.error(f"Failed to insert item {user_id}: {e}")
            conn.rollback()
            continue

    conn.commit()
    cursor.close()
    conn.close()
    
    logging.info(f"Migration complete! Successfully migrated {success_count}/{len(items)} records to RDS.")

if __name__ == "__main__":
    DDB_TABLE = "ProductionUsers"
    RDS_ENDPOINT = "my-rds-db.cluster-xxxxxx.us-east-1.rds.amazonaws.com"
    DB_NAME = "myappdb"
    DB_USER = "admin"
    DB_PASS = "SuperSecretPassword123!"
    
    migrate_dynamodb_to_rds(DDB_TABLE, RDS_ENDPOINT, DB_NAME, DB_USER, DB_PASS)
```

### Bash Approach (S3 Export)
**How to use:** 
1. Ensure the AWS CLI is configured with permissions to access DynamoDB and S3.
2. Update the `DDB_TABLE_ARN` and `S3_BUCKET` variables in the script.
3. Run the script: `bash dynamodb_to_rds_migration.sh`.
4. Once completed, connect to your RDS instance and run the provided SQL command to natively ingest the S3 data.

```bash
#!/bin/bash

# Script: DynamoDB to RDS Migration via S3 Export
DDB_TABLE_ARN="arn:aws:dynamodb:us-east-1:123456789012:table/ProductionUsers"
S3_BUCKET="my-migration-bucket-123"
EXPORT_FORMAT="DYNAMODB_JSON"

echo "Step 1: Requesting DynamoDB to export table data to S3..."

EXPORT_ARN=$(aws dynamodb export-table-to-point-in-time \
    --table-arn "$DDB_TABLE_ARN" \
    --s3-bucket "$S3_BUCKET" \
    --export-format "$EXPORT_FORMAT" \
    --query 'ExportDescription.ExportArn' \
    --output text)

echo "Export started. Export ARN: $EXPORT_ARN"

echo "Step 2: Waiting for the export to finish..."

STATUS="IN_PROGRESS"
while [ "$STATUS" != "COMPLETED" ]; do
    sleep 30
    STATUS=$(aws dynamodb describe-export \
        --export-arn "$EXPORT_ARN" \
        --query 'ExportDescription.ExportStatus' \
        --output text)
    echo "Current Status: $STATUS"
    
    if [ "$STATUS" == "FAILED" ]; then
        echo "Export failed! Check your DynamoDB and S3 permissions."
        exit 1
    fi
done

echo "Step 3: Export completed to s3://$S3_BUCKET/AWSDynamoDB/"
echo "Step 4: Connect to Aurora PostgreSQL and run:"
echo "SELECT aws_s3.table_import_from_s3('users_table', '', '(format json)', '$S3_BUCKET', 'AWSDynamoDB/export-id/data/');"
```

---

## 2. S3 to S3 Migration

A script to efficiently copy objects from one S3 bucket to another within the AWS network.

**How to use:** 
1. Ensure `boto3` is installed and AWS credentials are valid.
2. Replace the `SOURCE` and `DEST` bucket names at the bottom of the script.
3. Run `python3 s3_to_s3_migration.py`.

```python
import boto3
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def migrate_s3_bucket(source_bucket_name, dest_bucket_name):
    """Migrates all objects from one S3 bucket to another."""
    s3 = boto3.resource('s3')
    
    source_bucket = s3.Bucket(source_bucket_name)
    dest_bucket = s3.Bucket(dest_bucket_name)
    
    logging.info(f"Starting migration from {source_bucket_name} to {dest_bucket_name}")
    
    for obj in source_bucket.objects.all():
        copy_source = {
            'Bucket': source_bucket_name,
            'Key': obj.key
        }
        try:
            logging.info(f"Copying {obj.key}...")
            dest_bucket.copy(copy_source, obj.key)
        except Exception as e:
            logging.error(f"Failed to copy {obj.key}: {e}")
            
    logging.info("Migration completed successfully.")

if __name__ == "__main__":
    SOURCE = "my-legacy-data-bucket-123"
    DEST = "my-new-secure-bucket-456"
    migrate_s3_bucket(SOURCE, DEST)
```

---

## 3. S3 to EFS Download

Downloads all objects from an S3 bucket to a local path (which should be your EFS mount point).

**How to use:** 
1. Ensure the script is run on the EC2 instance where EFS is mounted.
2. Update the `BUCKET` name and `EFS_PATH` to point to the actual mount directory.
3. Run `python3 s3_to_efs_download.py`.

```python
import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def migrate_s3_to_efs(bucket_name, efs_mount_point):
    """Downloads all objects from an S3 bucket to a local directory (EFS)."""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    if not os.path.exists(efs_mount_point):
        logging.error(f"EFS mount point {efs_mount_point} does not exist!")
        return

    logging.info(f"Starting download from {bucket_name} to {efs_mount_point}")
    
    for obj in bucket.objects.all():
        local_file_path = os.path.join(efs_mount_point, obj.key)
        
        local_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            
        try:
            logging.info(f"Downloading {obj.key}...")
            bucket.download_file(obj.key, local_file_path)
        except Exception as e:
            logging.error(f"Failed to download {obj.key}: {e}")
            
    logging.info("S3 to EFS migration completed.")

if __name__ == "__main__":
    BUCKET = "my-training-data-bucket"
    EFS_PATH = "/mnt/efs/migrated_data"
    migrate_s3_to_efs(BUCKET, EFS_PATH)
```

---

## 4. Local Directory to S3 Sync

Uses the AWS CLI to incrementally sync files from a local directory (or NAS/EBS) to an S3 bucket.

**How to use:** 
1. Update `LOCAL_PATH` and `S3_URI` in the script.
2. Run `bash local_to_s3_sync.sh`.

```bash
#!/bin/bash

# Script: Local to S3 Migration Sync
LOCAL_PATH="/data/legacy_archives/"
S3_URI="s3://my-cloud-archive-bucket/imports/"

echo "Starting migration from $LOCAL_PATH to $S3_URI..."

aws s3 sync "$LOCAL_PATH" "$S3_URI"

if [ $? -eq 0 ]; then
    echo "Migration completed successfully!"
else
    echo "Migration encountered an error."
fi
```

---

## 5. EBS Snapshot Cross-Region Migration

Creates a snapshot of an EBS volume and copies it to another AWS Region.

**How to use:** 
1. Update the `SOURCE_VOLUME_ID`, `SOURCE_REGION`, and `DEST_REGION`.
2. Run `bash ebs_snapshot_migration.sh`. The script will wait until the snapshot is complete before initiating the cross-region copy.

```bash
#!/bin/bash

# Script: EBS Volume Cross-Region Migration
SOURCE_VOLUME_ID="vol-0123456789abcdef0"
SOURCE_REGION="us-east-1"
DEST_REGION="us-west-2"

echo "Step 1: Creating snapshot of volume $SOURCE_VOLUME_ID in $SOURCE_REGION..."

SNAPSHOT_ID=$(aws ec2 create-snapshot \
    --volume-id "$SOURCE_VOLUME_ID" \
    --description "Migration snapshot for $SOURCE_VOLUME_ID" \
    --region "$SOURCE_REGION" \
    --query 'SnapshotId' \
    --output text)

echo "Created Snapshot ID: $SNAPSHOT_ID"

echo "Step 2: Waiting for snapshot to complete..."
aws ec2 wait snapshot-completed \
    --snapshot-ids "$SNAPSHOT_ID" \
    --region "$SOURCE_REGION"

echo "Snapshot completed. Step 3: Copying snapshot to $DEST_REGION..."

NEW_SNAPSHOT_ID=$(aws ec2 copy-snapshot \
    --source-region "$SOURCE_REGION" \
    --source-snapshot-id "$SNAPSHOT_ID" \
    --description "Copied from $SOURCE_REGION" \
    --region "$DEST_REGION" \
    --query 'SnapshotId' \
    --output text)

echo "Migration successful! New Snapshot ID in $DEST_REGION is: $NEW_SNAPSHOT_ID"
```
