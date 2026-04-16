import boto3
import os
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_PATH / 'output' / 'quotes.csv'
load_dotenv(BASE_PATH / '.env')

def __require_env(key):
    value = os.getenv(key)
    if value is None:
        logger.debug(f"Environment variable '{key}' is required but not set.")
        
    return value

def upload_quotes():
    logger.info('Starting upload of quotes to S3 bucket...')
    
    ACCESS_KEY = __require_env("ACCESS_KEY")
    ACCESS_SECRET = __require_env("ACCESS_SECRET")
    
    s3 = boto3.client('s3',
                    aws_access_key_id=ACCESS_KEY,           # Access credentials will only be used in local environment
                    aws_secret_access_key=ACCESS_SECRET
                )

    BUCKET_NAME = __require_env("BUCKET_NAME")
    BUCKET_FILE = __require_env("BUCKET_FILE")

    # Upload the file
    try:
        s3.upload_file(OUTPUT_PATH, BUCKET_NAME, BUCKET_FILE)
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        raise

    logger.info(f"Successfully uploaded {OUTPUT_PATH} to {BUCKET_NAME}")