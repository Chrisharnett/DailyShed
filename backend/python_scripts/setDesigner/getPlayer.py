from dotenv import load_dotenv
import boto3
import os

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
user_table = dynamodb.Table(os.environ['USER_TABLE'])

def getPlayerData(sub):
    try:
        response = user_table.get_item(
            Key={'sub': sub},
        )
        if 'Item' in response:
            player = response['Item']
            return player
        else:
            return 'Player not found'
    except Exception as e:
        print(e)
        return 'error'