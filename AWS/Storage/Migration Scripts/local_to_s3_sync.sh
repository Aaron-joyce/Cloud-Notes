#!/bin/bash

# ==============================================================================
# Script: Local to S3 Migration Sync
# Description: Uses the AWS CLI to securely migrate a local directory (like an 
#              on-premise NAS or attached EBS volume) into an Amazon S3 bucket.
# ==============================================================================

# ---------------------------------------------------------
# API Variables Explained:
# ---------------------------------------------------------
# LOCAL_PATH: The absolute path to the directory on your server containing the data.
#   -> Retrieve from: Your local terminal/server (e.g., /data/archives/)
# S3_URI: The exact uniform resource identifier for the destination S3 bucket.
#   -> Retrieve from: AWS Console > Amazon S3 > Buckets (Format: s3://bucket-name/)

LOCAL_PATH="/data/legacy_archives/"
S3_URI="s3://my-cloud-archive-bucket/imports/"

echo "Starting migration from $LOCAL_PATH to $S3_URI..."

# The 'aws s3 sync' command is the most robust way to migrate files to S3 via CLI.
# What this block does:
# 1. Compares the local directory to the S3 bucket.
# 2. Only uploads files that are new or have been modified (saving bandwidth).
# 3. Uses multi-threading automatically for fast parallel uploads.
aws s3 sync "$LOCAL_PATH" "$S3_URI"

# Check the exit status of the sync command
if [ $? -eq 0 ]; then
    echo "Migration completed successfully!"
else
    echo "Migration encountered an error. Please check your AWS credentials and network connection."
fi
