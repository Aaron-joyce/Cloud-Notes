#!/bin/bash

# ==============================================================================
# Script: DynamoDB to RDS Migration via S3 Export
# Description: For large DynamoDB tables, a python scan is too slow. The best 
#              practice is to use the AWS CLI to export DynamoDB to S3 in JSON, 
#              and then use a native database command to import from S3 to RDS.
# ==============================================================================

# ---------------------------------------------------------
# API Variables Explained:
# ---------------------------------------------------------
# DDB_TABLE_ARN: The Amazon Resource Name of the DynamoDB table.
#   -> Retrieve from: AWS Console > DynamoDB > Tables > Additional info
# S3_BUCKET: The name of the S3 bucket to store the intermediate export.
#   -> Retrieve from: AWS Console > S3
# RDS_IDENTIFIER: The name of your RDS Database instance.
#   -> Retrieve from: AWS Console > RDS > Databases

DDB_TABLE_ARN="arn:aws:dynamodb:us-east-1:123456789012:table/ProductionUsers"
S3_BUCKET="my-migration-bucket-123"
EXPORT_FORMAT="DYNAMODB_JSON"

echo "Step 1: Requesting DynamoDB to export table data to S3..."

# The 'aws dynamodb export-table-to-point-in-time' command takes a snapshot of your 
# DynamoDB table without consuming read capacity units (RCUs) and saves it to S3.
EXPORT_ARN=$(aws dynamodb export-table-to-point-in-time \
    --table-arn "$DDB_TABLE_ARN" \
    --s3-bucket "$S3_BUCKET" \
    --export-format "$EXPORT_FORMAT" \
    --query 'ExportDescription.ExportArn' \
    --output text)

echo "Export started. Export ARN: $EXPORT_ARN"

echo "Step 2: Waiting for the export to finish (this can take several minutes to hours depending on table size)..."

# Poll the describe-export API until the status is 'COMPLETED'
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
echo ""
echo "Step 4: Import into RDS"
echo "Because RDS engines differ (MySQL vs PostgreSQL), you must run a native SQL command on your database to ingest the S3 files."
echo ""
echo "For Aurora PostgreSQL, connect to your database and run:"
echo "SELECT aws_s3.table_import_from_s3("
echo "  'users_table',"
echo "  '',"
echo "  '(format json)',"
echo "  '$S3_BUCKET',"
echo "  'AWSDynamoDB/export-id/data/'"
echo ");"
