import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

def upload_file_to_s3(file_obj, file_name):
    try:
        s3.upload_fileobj(file_obj, os.getenv("AWS_BUCKET_NAME"), file_name, ExtraArgs={'ACL': 'public-read'})
    except FileNotFoundError:
        print(f"The file was not found: {file_name}")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except PartialCredentialsError:
        print("Incomplete credentials")
        return None
    return f"https://{os.getenv("AWS_BUCKET_NAME")}.s3.{os.getenv("AWS_REGION")}.amazonaws.com/{file_name}"
