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
    # ---------------------------------------------------------
    # API Variables Explained:
    # ---------------------------------------------------------
    # table_name: The exact string name of your DynamoDB table.
    #   -> Retrieve from: AWS Console > DynamoDB > Tables
    # rds_host: The Endpoint URL of your RDS instance.
    #   -> Retrieve from: AWS Console > RDS > Databases > [Your DB] > Connectivity & security
    
    # 1. Initialize DynamoDB Resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # 2. Connect to RDS PostgreSQL
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
    
    # 3. Scan the DynamoDB table (Note: For massive tables, an S3 export is better)
    # The scan() API reads every item in the table.
    response = table.scan()
    items = response.get('Items', [])
    
    # Handle pagination if the table is larger than 1MB
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))

    logging.info(f"Retrieved {len(items)} items from DynamoDB. Starting RDS insertion...")

    # 4. Insert items into RDS
    # This requires a pre-existing table in RDS that matches your DynamoDB data structure.
    insert_query = """
        INSERT INTO users (user_id, email, created_at) 
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """
    
    success_count = 0
    for item in items:
        try:
            # Extract data from the DynamoDB dictionary. Use .get() to handle missing attributes safely.
            user_id = item.get('UserId')
            email = item.get('Email', 'no-email@example.com')
            created_at = item.get('CreatedAt', '1970-01-01')
            
            # Execute the SQL insertion
            cursor.execute(insert_query, (user_id, email, created_at))
            success_count += 1
            
        except Exception as e:
            logging.error(f"Failed to insert item {user_id}: {e}")
            conn.rollback() # Rollback the failed transaction
            continue

    # Commit all successful inserts
    conn.commit()
    cursor.close()
    conn.close()
    
    logging.info(f"Migration complete! Successfully migrated {success_count}/{len(items)} records to RDS.")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    DDB_TABLE = "ProductionUsers"
    RDS_ENDPOINT = "my-rds-db.cluster-xxxxxx.us-east-1.rds.amazonaws.com"
    DB_NAME = "myappdb"
    DB_USER = "admin"
    DB_PASS = "SuperSecretPassword123!"
    
    migrate_dynamodb_to_rds(DDB_TABLE, RDS_ENDPOINT, DB_NAME, DB_USER, DB_PASS)
