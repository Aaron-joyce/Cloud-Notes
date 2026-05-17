To migrate data out of DynamoDB without managed services like Glue or DMS, you essentially reverse the ETL process. The most common manual methods involve using the DynamoDB Scan API or S3 Export, followed by a custom loader script.
Here is a detailed breakdown and a markdown file structure for this process.
1. The Strategy: S3 Export vs. Scan API
| Method | Best For | Pros | Cons |
|---|---|---|---|
| S3 Export | Large Datasets (GBs/TBs) | No impact on table performance (no RCU used). | Requires Point-in-Time Recovery (PITR) to be enabled. |
| Scan API | Small/Medium Datasets | Simple to script; no extra AWS features needed. | Consumes Read Capacity Units (RCU); can throttle production apps. |
2. Implementation Guide (S3 + Python)
Step 1: Export to S3
 * Enable PITR (Point-in-Time Recovery) on your DynamoDB table.
 * Use the Console or CLI: aws dynamodb export-table-to-point-in-time --table-arn <arn> --s3-bucket <bucket-name>.
 * This generates compressed JSON files in S3.
Step 2: Extraction Script (Python)
Since DynamoDB exports are in "DynamoDB JSON" format (e.g., {"Email": {"S": "test@me.com"}}), you must unmarshall them into standard JSON before inserting them into a new database (like RDS).
import boto3
import json
import gzip
from boto3.dynamodb.types import TypeDeserializer

# Initialize Deserializer to convert DynamoDB JSON to standard Python dicts
deserializer = TypeDeserializer()

def unmarshall(dynamo_json):
    """Converts {'Name': {'S': 'Aaron'}} to {'Name': 'Aaron'}"""
    return {k: deserializer.deserialize(v) for k, v in dynamo_json.items()}

def process_s3_export(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    
    # Exported files are usually Gzipped
    with gzip.GzipFile(fileobj=response['Body']) as gf:
        for line in gf:
            # Each line is a DynamoDB record
            record = json.loads(line)
            data = unmarshall(record['Item'])
            
            # --- LOAD LOGIC HERE ---
            # e.g., cursor.execute("INSERT INTO table ...", (data['Email'], ...))
            print(f"Ready to load: {data}")

# Example Usage
# process_s3_export('my-migration-bucket', 'export-prefix/data/file.json.gz')

3. Migration Documentation (Markdown)
Copy and save the following as DYNAMODB_OUTBOUND_MIGRATION.md:
# Manual Migration: Exporting from DynamoDB

This guide explains how to manually extract data from DynamoDB for migration to RDS, S3, or another NoSQL provider without Glue or DMS.

## 1. Extraction Workflow
We utilize the **S3 Export** feature because it provides a consistent snapshot without consuming your table's Read Capacity Units (RCU).

1. **Enable PITR:** Ensure Point-in-Time Recovery is active on the source table.
2. **Request Export:** Initiate the export to an S3 bucket via the AWS CLI or SDK.
3. **Download/Process:** Read the resulting `.json.gz` files using a processing script.

## 2. Data Transformation (The "Unmarshalling" Problem)
DynamoDB stores data in a specific JSON format that includes type descriptors. You must strip these before moving to a relational database.

**Example Source:**
```json
{ "user_id": {"N": "101"}, "active": {"BOOL": true} }

Target Format:
{ "user_id": 101, "active": true }

3. Migration Script Template (Python)
import boto3
import json
from boto3.dynamodb.types import TypeDeserializer

def migrate_from_dynamo():
    # 1. Setup
    s3 = boto3.resource('s3')
    deserializer = TypeDeserializer()
    bucket = s3.Bucket('your-export-bucket')

    # 2. Iterate through export files
    for obj in bucket.objects.filter(Prefix='AWSDynamoDB/'):
        if obj.key.endswith('.json.gz'):
            # Logic to unzip and read line by line
            # logic to unmarshall using deserializer.deserialize()
            # logic to INSERT into target DB
            pass

    print("Extraction complete.")

4. Operational Considerations
 * Schema Mapping: Ensure your target (RDS) has the correct table constraints (VARCHAR lengths, Primary Keys) before loading.
 * Large Objects: If your DynamoDB items contain large Map or List types, decide whether to flatten them into columns or store them as JSON/BLOB in the target.
 * Batch Loading: When moving to RDS, use executemany() or COPY commands rather than individual INSERT statements to improve performance.

---

### Pro-Tip for IndiaSkills
During the competition, if you are asked to move data **between** DynamoDB tables in different regions, the fastest manual way is to use a **Lambda function** triggered by **DynamoDB Streams**. This handles the migration in real-time as data changes.

Would you like to see the Lambda script for real-time migration via Streams?

