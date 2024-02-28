import boto3
from dotenv import load_dotenv
import os

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
exercise_table = dynamodb.Table(os.environ['EXERCISE_TABLE'])
exercise_log_table = dynamodb.Table(os.environ['EXERCISE_LOG_TABLE'])

def fetchExerciseDetails(exercise):
    response = exercise_table.get_item(
        Key={
            'fileName': exercise.get('exerciseName')
        }
    )
    if response['Item']:
        return response['Item']
    else: return None

def fetchExercisesFromLog(exercises):
    table = os.environ['EXERCISE_TABLE']
    keys_to_get = [{'fileName': exercise.get('exerciseName')} for exercise in exercises]

    request_items = {
        table: {
            'Keys': keys_to_get,
            'ConsistentRead': True
        }
    }

    response = dynamodb.batch_get_item(RequestItems=request_items)

    if response['Responses'][table]:
        return response['Responses'][table]
    else:
        return None