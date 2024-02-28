import abjad
import boto3
import os
from setDesigner.exerciseObjects import Exercise
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
exercise_table = dynamodb.Table(os.environ['EXERCISE_TABLE'])
bucket_name = os.environ['IMAGE_BUCKET']

def exerciseImageMaker(exercise):
    exerciseName = exercise['exerciseName']
    pitches = exercise['notePattern']
    rhythm = exercise['rhythmPattern']
    key = exercise['key']
    mode = exercise['mode']
    collectionTitle = exercise['collectionTitle']
    fileName = exercise['fileName']
    imageURL = exercise['imageURL']
    description = exercise['description']
    preamble = exercise.get('preamble', r"#(set-global-staff-size 28)")

    exercise = Exercise(pitches, rhythm, key, mode, preamble)
    score = exercise.buildScore
    lilypond_file = abjad.LilyPondFile([preamble, score])

    current_file_directory = os.path.dirname(__file__)

    absolutePath = os.path.join(current_file_directory, "../", "temp/")

    localPath = os.path.join(absolutePath + fileName)

    abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)

    s3BucketName = bucket_name
    png = os.path.join(localPath + ".cropped.png")

    s3_client = boto3.client("s3")
    s3_client.upload_file(png, s3BucketName, (fileName+'.cropped.png'))

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