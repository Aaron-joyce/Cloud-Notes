import boto3
import logging

# Set up basic logging to track the migration process
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def migrate_s3_bucket(source_bucket_name, dest_bucket_name):
    """
    Migrates all objects from one S3 bucket to another.
    """
    # ---------------------------------------------------------
    # API Variables Explained:
    # ---------------------------------------------------------
    # source_bucket_name: The exact string name of the origin bucket.
    #   -> Retrieve from: AWS Console > Amazon S3 > Buckets (Origin)
    # dest_bucket_name: The exact string name of the destination bucket.
    #   -> Retrieve from: AWS Console > Amazon S3 > Buckets (Destination)
    
    # Initialize the S3 resource using boto3. 
    # This automatically picks up credentials from your environment (~/.aws/credentials)
    s3 = boto3.resource('s3')
    
    source_bucket = s3.Bucket(source_bucket_name)
    dest_bucket = s3.Bucket(dest_bucket_name)
    
    logging.info(f"Starting migration from {source_bucket_name} to {dest_bucket_name}")
    
    # This block iterates over every object currently inside the source bucket.
    # `source_bucket.objects.all()` uses the S3 ListObjectsV2 API under the hood.
    for obj in source_bucket.objects.all():
        
        # 'copy_source' is a dictionary required by the S3 Copy API.
        # It tells AWS exactly where to copy the data from.
        # - 'Bucket': The origin bucket name
        # - 'Key': The exact file path/name of the object inside the bucket
        copy_source = {
            'Bucket': source_bucket_name,
            'Key': obj.key
        }
        
        try:
            logging.info(f"Copying {obj.key}...")
            # The copy() method calls the S3 CopyObject API.
            # This is highly efficient because the data transfer happens entirely 
            # within the AWS network; it does not download the file to your local machine.
            dest_bucket.copy(copy_source, obj.key)
        except Exception as e:
            logging.error(f"Failed to copy {obj.key}: {e}")
            
    logging.info("Migration completed successfully.")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace these with your actual bucket names
    SOURCE = "my-legacy-data-bucket-123"
    DEST = "my-new-secure-bucket-456"
    
    migrate_s3_bucket(SOURCE, DEST)
