import os
from setDesigner.exerciseImageMaker import exerciseImageMaker
from dotenv import load_dotenv
import boto3

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])


exercise_table = dynamodb.Table(os.environ['EXERCISE_TABLE'])
bucket_name = os.environ['IMAGE_BUCKET']

def createExercise(pitches, rhythm, exerciseDetails):
    key = exerciseDetails.get('key')
    mode = exerciseDetails.get('mode')
    exerciseName = ''
    collectionTitle = f"{key.upper()} {mode.title()} {pitches.get('collectionTitle')} "
    if pitches.get('collectionTitle') != 'Long Tone':
        collectionTitle += f"in {rhythm.get('rhythmDescription').replace('_', ' ')}s"
        exerciseName += f"{pitches.get('direction').title()} pattern {getDirectionPrep(pitches.get('direction'))} the {str(max(int(number) for number in pitches.get('notePattern')))}"
    else:
        exerciseName += f"{pitches.get('notePatternType').replace('_', ' ').title()}"
        collectionTitle += f""
    fileName = f"{collectionTitle.lower().replace(' ', '_')}_{exerciseName.lower().replace(' ', '_')}_{pitches.get('notePatternId')}_{rhythm.get('rhythmPatternId')}"
    imageURL = f"https://{bucket_name}.s3.amazonaws.com/{fileName}.cropped.png"
    description = pitches.get('description')
    exercise = {
        'exerciseName': exerciseName,
        'notePattern': pitches,
        'rhythmPattern': rhythm,
        'key': key,
        'mode': mode,
        'collectionTitle': collectionTitle,
        'fileName': fileName,
        'imageURL': imageURL,
        'description': description
    }
    response = exercise_table.get_item(
        Key={
            'fileName': fileName
        }
    )
    if not 'Item' in response:
        image = exerciseImageMaker(exercise)

    return exercise

def getDirectionPrep(direction):
    if direction == "ascending" or direction == "ascending descending":
        return 'to'
    elif direction == "descending" or direction == "descending ascending":
        return 'from'