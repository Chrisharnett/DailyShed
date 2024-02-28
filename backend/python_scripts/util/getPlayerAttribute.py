import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
user_table = dynamodb.Table(os.environ['USER_TABLE'])

def getPlayerAttribute(sub, projection):
    try:
        response = user_table.get_item(
            Key={'sub': sub},
            ProjectionExpression=projection
        )
        if 'Item' in response:
            player = response['Item']
            return player
        else:
            return 'Player not found'
    except Exception as e:
        print(e)
        return 'error'