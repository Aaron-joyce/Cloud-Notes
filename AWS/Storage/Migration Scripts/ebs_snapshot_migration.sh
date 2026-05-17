#!/bin/bash

# ==============================================================================
# Script: EBS Volume Cross-Region Migration
# Description: Takes an existing EBS volume, creates a snapshot, and copies 
#              that snapshot to a different AWS Region for disaster recovery.
# ==============================================================================

# ---------------------------------------------------------
# API Variables Explained:
# ---------------------------------------------------------
# SOURCE_VOLUME_ID: The unique ID of the EBS volume you want to migrate.
#   -> Retrieve from: AWS Console > EC2 > Elastic Block Store > Volumes (e.g., vol-0123456789abcdef0)
# SOURCE_REGION: The AWS region where the volume currently exists.
#   -> Retrieve from: AWS Console (top right corner, e.g., us-east-1)
# DEST_REGION: The target AWS region where you want the snapshot copied to.
#   -> Retrieve from: AWS Region documentation (e.g., us-west-2)

SOURCE_VOLUME_ID="vol-0123456789abcdef0"
SOURCE_REGION="us-east-1"
DEST_REGION="us-west-2"

echo "Step 1: Creating snapshot of volume $SOURCE_VOLUME_ID in $SOURCE_REGION..."

# 'aws ec2 create-snapshot' calls the CreateSnapshot API.
# The --query parameter extracts just the pure Snapshot ID from the JSON response.
# The --output text ensures we get a clean string without quotes.
SNAPSHOT_ID=$(aws ec2 create-snapshot \
    --volume-id "$SOURCE_VOLUME_ID" \
    --description "Migration snapshot for $SOURCE_VOLUME_ID" \
    --region "$SOURCE_REGION" \
    --query 'SnapshotId' \
    --output text)

echo "Created Snapshot ID: $SNAPSHOT_ID"

echo "Step 2: Waiting for snapshot to complete (this may take a while depending on volume size)..."
# The 'wait' command polls the DescribeSnapshots API until the status changes to 'completed'.
aws ec2 wait snapshot-completed \
    --snapshot-ids "$SNAPSHOT_ID" \
    --region "$SOURCE_REGION"

echo "Snapshot completed. Step 3: Copying snapshot to $DEST_REGION..."

# 'aws ec2 copy-snapshot' calls the CopySnapshot API.
# This moves the block-level backup from the source region across the AWS backbone to the destination.
NEW_SNAPSHOT_ID=$(aws ec2 copy-snapshot \
    --source-region "$SOURCE_REGION" \
    --source-snapshot-id "$SNAPSHOT_ID" \
    --description "Copied from $SOURCE_REGION" \
    --region "$DEST_REGION" \
    --query 'SnapshotId' \
    --output text)

echo "Migration successful! New Snapshot ID in $DEST_REGION is: $NEW_SNAPSHOT_ID"
