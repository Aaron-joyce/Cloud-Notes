import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def migrate_s3_to_efs(bucket_name, efs_mount_point):
    """
    Downloads all objects from an S3 bucket and saves them to a local directory.
    In AWS, this script would run on an EC2 instance where the EFS file system 
    is mounted to the 'efs_mount_point' path.
    """
    # ---------------------------------------------------------
    # API Variables Explained:
    # ---------------------------------------------------------
    # bucket_name: The name of the S3 bucket holding the source data.
    #   -> Retrieve from: AWS Console > Amazon S3 > Buckets
    # efs_mount_point: The absolute local path where the EFS volume is mounted.
    #   -> Retrieve from: EC2 terminal (e.g., run `df -h` to see mounted paths like /mnt/efs)
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    # Ensure the target EFS directory exists before downloading
    if not os.path.exists(efs_mount_point):
        logging.error(f"EFS mount point {efs_mount_point} does not exist!")
        return

    logging.info(f"Starting download from {bucket_name} to {efs_mount_point}")
    
    # Iterate through every object in the bucket
    for obj in bucket.objects.all():
        # Construct the local file path by joining the EFS mount point with the S3 object key.
        # S3 keys can contain slashes (e.g., "folder/file.txt"), which os.path.join handles.
        local_file_path = os.path.join(efs_mount_point, obj.key)
        
        # S3 "folders" are just prefixes in the object key. 
        # We must create the local directory structure if it doesn't exist.
        local_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            
        try:
            logging.info(f"Downloading {obj.key}...")
            # download_file() calls the S3 GetObject API.
            # Unlike the copy() API, this physically pulls the data over the network
            # and writes it to the attached EFS storage volume.
            bucket.download_file(obj.key, local_file_path)
        except Exception as e:
            logging.error(f"Failed to download {obj.key}: {e}")
            
    logging.info("S3 to EFS migration completed.")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace these values
    BUCKET = "my-training-data-bucket"
    EFS_PATH = "/mnt/efs/migrated_data"
    
    migrate_s3_to_efs(BUCKET, EFS_PATH)
