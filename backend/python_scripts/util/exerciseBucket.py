import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

load_dotenv()

def dropItInTheBucket(png, fileName):
    s3 = boto3.client("s3")
    s3.upload_file(png, os.environ['IMAGE_BUCKET'], (fileName + '.png'))
    # s3_client.upload_file(png, s3BucketName, (fileName + '.cropped.png'))

def imageURL(filename):
    return f"https://{os.environ['IMAGE_BUCKET']}.s3.amazonaws.com/{filename()}"

def checkTheBucketForImage(fileName):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=os.environ['IMAGE_BUCKET'], Key=fileName)
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e
    except (NoCredentialsError, PartialCredentialsError):
        print("Credentials not available.")
        return False
