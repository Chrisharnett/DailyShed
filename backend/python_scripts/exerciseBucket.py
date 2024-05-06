import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def dropItInTheBucket(png, fileName):
    s3_client = boto3.client("s3")
    s3_client.upload_file(png, os.environ['IMAGE_BUCKET'], (fileName + '.png'))
    # s3_client.upload_file(png, s3BucketName, (fileName + '.cropped.png'))

def imageURL(filename):
    return f"https://{os.environ['IMAGE_BUCKET']}.s3.amazonaws.com/{filename()}"
