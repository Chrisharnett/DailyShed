import os
import abjad
import boto3
from exerciseObjects import Exercise


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
exercise_table = dynamodb.Table('Daily_Shed_Exercises')
bucket_name = 'mysaxpracticeexercisebucket'

# 
def lambdaHandler(event):
    exerciseName = event['exerciseName']
    pitches = event['pitches']
    rhythm = event['rhythm']
    key = event['key']
    mode = event['mode']
    collectionTitle = event['collectionTitle']
    fileName = event['fileName']
    imageURL = event['imageURL']
    description = event['description']
    preamble = event.get('preamble', r"#(set-global-staff-size 28)")

    exercise = Exercise()
    lilypond_file = abjad.LilyPondFile([preamble, exercise.buildScore])

    current_file_directory = os.path.dirname(__file__)

    absolutePath = os.path.join(current_file_directory, "..", "temp/")

    localPath = os.path.join(absolutePath + fileName)

    abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)

    s3BucketName = bucket_name
    png = os.path.join(localPath + ".cropped.png")

    s3_client = boto3.client("s3")
    s3_client.upload_file(png, s3BucketName, fileName)

    ly = os.path.join(localPath + ".ly")

    os.remove(png)
    os.remove(ly)

    response = exercise_table.put_item(
        Item={
            'exerciseName': exerciseName,
            'notePattern': pitches,
            'rhythmPattern': rhythm,
            'key': key,
            'mode': mode,
            'collectionTitle': collectionTitle,
            'fileName': fileName,
            'imageURL': imageURL,
            'description': description,
        }
    )
    return response