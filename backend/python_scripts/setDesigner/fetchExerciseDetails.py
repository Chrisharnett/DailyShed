import boto3
from dotenv import load_dotenv
import os

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
exercise_table = dynamodb.Table(os.environ['EXERCISE_TABLE'])

def fetchExerciseDetails(exercise):
    response = exercise_table.get_item(
        Key={
            'fileName': exercise.get('fileName')
        }
    )
    if response['Items']:
        return response['Items']
    else: return None