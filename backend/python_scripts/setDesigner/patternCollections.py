import os
import boto3
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
collection_table = dynamodb.Table(os.environ['COLLECTION_TABLE'])

def getCollection(collectionType):
    try:
        response = collection_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('collectionType').eq(collectionType))

        if 'Items' in response:
            return response['Items']
        else:
            return 'Collections not found'
    except Exception as e:
        print('ERROR WITH COLLECTIONS: ', e)
        return 'error'
