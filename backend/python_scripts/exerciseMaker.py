

# import debugpy
from objects.collection import Collection
from objects.exerciseObjects import Exercise
from flask import Flask, request, jsonify
from flask_cors import CORS
from objects.player import Player
from objects.practiceSet import PracticeSet
from notePatternGenerator import stepwiseScaleNotePatterns, singleNoteLongToneWholeNotes
from rhythmPatternGenerator import quarterNoteRhythms, singleNoteWholeToneRhythms
import boto3
from datetime import datetime

# debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

s3_client = boto3.client("s3")


@app.route("/")
def home():
    return "Connected"


@app.route("/getManySets", methods=["GET", "POST"])
def getManySets():
    try:
        bucketName = "mysaxpracticeexercisebucket"
        data = request.get_json()
        player = Player(
            data["player"]["previousSet"],
            data["player"]["program"],
            data["player"]["exerciseHistory"],
        )
        numberOfSets = data["setsToCreate"]
        minNote = 1
        maxNote = 9
        notes = stepwiseScaleNotePatterns(
            minNote, maxNote, (2 * maxNote), "Scale to the Ninth"
        )
        notes.extend(
            singleNoteLongToneWholeNotes(minNote, maxNote, (2 * maxNote), "Long Tones")
        )
        rhythms = quarterNoteRhythms(4, 4)
        rhythms.extend(singleNoteWholeToneRhythms(4, 4))
        packageOfSets = []
        for i in range(numberOfSets):
            practiceSet = PracticeSet(player, notes, rhythms)
            nextSet = practiceSet.getNextSet()
            returnSet = []
            # for exercise in nextSet:
            for exercise in nextSet:
                try:
                    objectKey = exercise.exerciseFileName()
                    s3_client.head_object(Bucket=bucketName, Key=objectKey)
                except Exception as e:
                    exercise.createImage()
                e = exercise.serialize()
                returnSet.append(e)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                player.addExercise(exercise, timestamp, 8)
            player.setPreviousSet(nextSet)
            packageOfSets.append(returnSet)
        print(packageOfSets)
        return jsonify({"sets": packageOfSets, "player": player.serialize()})
    except Exception as err:
        return jsonify({"error": str(err)}), 400

@app.route("/getSet", methods=["GET", "POST"])
def getSet():
    try:
        # Set the incoming data needed
        bucketName = "mysaxpracticeexercisebucket"
        data = request.get_json()
        player = Player(data["previousSet"], data["program"], data["exerciseHistory"])

        # Set the details for the set. TODO: Send with JSON and do not hardcode
        minNote = 1
        maxNote = 9

        # Get relevant note and rhythm patterns
        notes = stepwiseScaleNotePatterns(
            minNote, maxNote, (2 * maxNote), "Scale to the 9", "quarter_note"
        )
        notes.extend(
            singleNoteLongToneWholeNotes(
                minNote, maxNote, (2 * maxNote), "Single Note Long Tones", "long_tone"
            )
        )
        rhythms = quarterNoteRhythms(4, 4)
        rhythms.extend(singleNoteWholeToneRhythms(4, 4))

        # Create a practice set object and build the next set.
        practiceSet = PracticeSet(player, notes, rhythms)
        currentSet = practiceSet.getNextSet()
        returnSet = []

        # Check if an image exists. If not (errer), create the images.
        for exercise in currentSet:
            try:
                objectKey = exercise.exerciseFileName()
                s3_client.head_object(Bucket=bucketName, Key=objectKey)
            except Exception as e:
                exercise.createImage()
            e = exercise.serialize()
            # url = exercise.imageURL()
            returnSet.append(e)

        # Return the set and player
        return jsonify({"returnSet": returnSet, "player": player.serialize()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

import boto3
import json
from collections import Counter
import random
import math
from serverlessFiles.createImageLambda import createExerciseImage
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('TheDailyShed_Users')
collection_table = dynamodb.Table('Daily_Shed_Collections')
exercise_table = dynamodb.Table('Daily_Shed_Exercises')
bucket_name = 'mysaxpracticeexercisebucket'

lambda_client = boto3.client('lambda')

@app.route("/lambdaGenerateSet", methods=["GET"])
def lambda_handler():
    try:
        event = request.get_json()
        userSub = event['sub']
        player = getPlayer(userSub)
        program = player.get('program')
        exerciseDetails = player.get('program').get('exerciseDetails')
        previousSet = player.get('previousSet')
        exerciseHistory = player.get('exerciseMetadata')
        newSet = []
        for i in range(len(exerciseDetails)):
            if exerciseDetails[i].get('reviewBool') and previousSet:
                notePatternType = exerciseDetails[i].get('notePatternType')

                notePatternOptions = [
                    exercise for exercise in exerciseHistory
                    if exercise.get('notePatternType') == notePatternType
                ]
                pitches = getReviewNotePattern(notePatternOptions, exerciseDetails[i], exerciseHistory)
                rhythm = getNewRhythmPattern(
                    getRhythmLength(pitches),
                    [collection for collection in getCollection('rhythm') if
                     collection.get('collectionType') == 'rhythm' and
                     exerciseDetails[i].get('rhythmMatcher') == collection.get('title')]
                )
                newSet.append(createExercise(pitches, rhythm, exerciseDetails[i]))

            else:
                pitches = getNewNotePattern(program, i)
                if previousSet:
                    # Get a review rhythm pattern for the collection type.
                    possibleRhythms = []
                    for exercise in exerciseHistory:
                        if (
                            exercise.get("rhythmMatcher")
                            == exerciseDetails[i].get('rhythmMatcher')
                        ):
                            possibleRhythms.append(exercise)
                    if 0 < len(possibleRhythms):
                        minPlays = getMinPlays(possibleRhythms)
                        rhythm = getRhythmReviewPattern(
                            possibleRhythms, minPlays, getRhythmLength(pitches), exerciseDetails[i]
                        )
                    else:
                        rhythm = getNewRhythmPattern(getRhythmLength(pitches), exerciseDetails[i]["rhythmMatcher"])
                else:
                    rhythmCollections = getCollection('rhythm')
                    matchingCollections = [collection for collection in rhythmCollections if
                                        exerciseDetails[i].get('rhythmMatcher') == collection.get('title')]
                    rhythm = next(
                        pattern for collection in matchingCollections for pattern in collection['patterns']
                        if pattern.get('rhythmDescription') == exerciseDetails[i].get('rhythmMatcher')
                        and rhythmNoteLength(pattern) == getRhythmLength(pitches)
                    )

                e = createExercise(pitches, rhythm, exerciseDetails[i])
                newSet.append(e)
        return {
            "statusCode": 200,
            "body": json.dumps({"set": newSet}),
            "headers": {
                "Content-Type": "application/json"
            },
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            },
        }

def getRhythmReviewPattern(possibleRhythms, min, length, exerciseDetails):
    rhythms = []
    for rhythm in possibleRhythms:
        if (
            rhythm.get("playCount") == min
            and rhythm.get("noteLength") == length
        ):
            rhythms.append(rhythm)
    if len(rhythms) == 0:
        rhythms = [
            getNewRhythmPattern(
                length,
                [collection for collection in getCollection('rhythm') if
                 collection.get('collectionType') == 'rhythm' and
                 exerciseDetails.get('rhythmMatcher') == collection.get('title')]
            )
        ]
        return rhythms[random.randint(0, len(rhythms) - 1)]
    r = fetchExerciseDetails(rhythms([random.randint(0, len(rhythms) - 1)])).get('rhythmPattern')
    return r

def getNewNotePattern(program, i):
    notePatternType = program.get('exerciseDetails')[i].get('notePatternType')
    collections = getCollection('notePattern')
    notePatternCollection = [
        pattern for collection in collections for pattern in collection['patterns'] if pattern.get('notePatternType') == notePatternType
    ]
    # Gets the next notePattern index for the player.
    for collection in program.get("collections"):
        if collection.get("notePatternType") == notePatternType:
            currentPlayerIndex = collection["index"]
            if currentPlayerIndex >= len(notePatternCollection):
                collection['index'] = -1
            else:
                collection['index'] = currentPlayerIndex + 1
            notePattern = notePatternCollection[
                ((int(currentPlayerIndex) + 1) )% len(notePatternCollection)
                ]
            notePattern['collectionTitle'] = collection.get('collectionTitle')
            return notePattern
    return None

def getDirectionPrep(direction):
    if direction == "ascending" or direction == "ascending descending":
        return 'to'
    elif direction == "descending" or direction == "descending ascending":
        return 'from'

def fetchExerciseDetails(exercise):
    response = exercise_table.get_item(
        Key={
            'fileName': exercise.get('fileName')
        }
    )
    if response['Items']:
        return response['Items']
    else: return None

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

    response = exercise_table.get_item(
        Key={
            'fileName': fileName
        }
    )
    if not 'Item' in response:
        # TODO: REPLACE LAMBDA CALL
        response = createExerciseImage(json.dumps({
            'exerciseName': exerciseName,
            'notePattern': pitches,
            'rhythmPattern': rhythm,
            'key': key,
            'mode': mode,
            'collectionTitle': collectionTitle,
            'fileName': fileName,
            'imageURL': imageURL,
            'description': description
        }, cls = DecimalEncoder))
        # response = lambda_client.invoke(
        #     FunctionName='createExerciseImage',  # The name of the Lambda function you're invoking
        #     InvocationType='Event',  # Use 'Event' for asynchronous execution. Use 'RequestResponse' for synchronous
        #     Payload=json.dumps({
        #         'exerciseName': exerciseName,
        #         'notePattern': pitches,
        #         'rhythmPattern': rhythm,
        #         'key': key,
        #         'mode': mode,
        #         'collectionTitle': collectionTitle,
        #         'fileName': fileName,
        #         'imageURL': imageURL,
        #         'description': description,
        #     }),
        # )

    return {
        'exerciseName': exerciseName,
        'collectionTitle': collectionTitle.title(),
        'key': key,
        "mode": mode,
        "imageFileName": fileName,
        "imageURL": imageURL,
        "description": description,
    }

def getPlayer(sub):
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

def rhythmPatternNoteLength(rhythmPattern):
    count = 0
    for r in rhythmPattern.get('rhythmPattern'):
        for n in r:
            if n.isdigit():
                count += 1
    n = sum(sublist.count("~") for sublist in rhythmPattern)
    count -= n
    return count

def getNewRhythmPattern(length, rhythmCollection):
    maxRhythmLength = max(rhythmPatternNoteLength(rhythmPattern) for collection in rhythmCollection for rhythmPattern in collection['patterns'])
    exactMatchRhythms = [rhythmPattern for collection in rhythmCollection for rhythmPattern in collection['patterns'] if rhythmPatternNoteLength(rhythmPattern) == length]
    if exactMatchRhythms:
        selectedRhythm = random.choice(exactMatchRhythms)
        return selectedRhythm
    else:
        return multipleBarRhythm(maxRhythmLength, rhythmCollection, length)

def rhythmNoteLength(rhythmPattern):
    count = 0
    for r in rhythmPattern.get('rhythmPattern'):
        for n in r:
            if n.isdigit():
                count += 1
    n = sum(sublist.count("~") for sublist in rhythmPattern.get("rhythmPattern"))
    count -= n
    return count

def multipleBarRhythm(maxRhythmLength, rhythms, length):
    minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
    measureNumber = 0
    remainder = length
    r = []
    id = ""
    while remainder > maxRhythmLength:
        possibleRhythms = [
            rhythmPattern for pattern in rhythms for rhythmPattern in pattern['patterns'] if length / minimumNumberOfMeasures <= rhythmNoteLength(rhythmPattern)
        ]
        if len(possibleRhythms) > 1:
            measure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
        else:
            measure = possibleRhythms[0]

        r.extend(measure.get('rhythmPattern'))
        id += str(measure.get('rhythmPatternId'))
        remainder -= rhythmNoteLength(measure)
    possibleRhythms = [rhythmPattern for pattern in rhythms for rhythmPattern in pattern['patterns'] if rhythmNoteLength(rhythmPattern) == remainder]
    lastMeasure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
    r.extend(lastMeasure.get('rhythmPattern'))
    id += f"#{str(lastMeasure.get('rhythmPatternId'))}"
    rhythmPattern = rhythms[0].get('patterns')[0]
    rhythmPattern['rhythmPattern'] = r
    rhythmPattern['rhythmPatternId'] = id
    return rhythmPattern

def getRhythmLength(pitches):
    if pitches.get('holdLastNote'):
        return len(pitches.get('notePattern')) - 1
    return len(pitches.get('notePattern'))

def getMinPlays(notePatternOptions):
    selectedExerciseCounts = Counter(
        notePattern.get('exercise').get('exerciseName') for notePattern in notePatternOptions
    )
    return selectedExerciseCounts[min(selectedExerciseCounts)]

def chooseDirection(notePattern, directionsPlayed):
    directions = [
        "ascending",
        "descending",
        "ascending descending",
        "descending ascending",
    ]
    index = len(directionsPlayed) - 1
    if 0 < index < 4:
        return directions[index]
    return directions[random.randint(0, len(directions) - 1)]

def descendingPattern(pattern):
    d = pattern.get('notePattern').copy()
    d.reverse()
    pattern['notePattern'] = d
    pattern['direction'] = 'descending'
    return pattern

def ascendingDescendingPattern(pattern):
    a = pattern.get('notePattern').copy()
    d = pattern.get('notePattern').copy()
    d.reverse()
    a.pop()
    a.extend(d)
    pattern['notePattern'] = a
    pattern['direction'] = 'ascending descending'
    return pattern

def descendingAscendingPattern(pattern):
    d = pattern.get('notePattern').copy()
    d.reverse()
    d.pop()
    d.extend(pattern.get("notePattern"))
    pattern['notePattern'] = d
    pattern['direction'] = 'descending ascending'
    return pattern

def getReviewNotePattern(notePatternOptions, details, exerciseHistory):
    minPlays = getMinPlays(notePatternOptions)
    reviewPatterns = [
        exercise
        for exercise in exerciseHistory
        if exercise.get('playCount') == minPlays
           and exercise.get("rhythmMatcher") == details.get('rhythmMatcher')]

    reviewPattern = reviewPatterns[random.randint(0, len(reviewPatterns) - 1)]
    pattern = fetchExerciseDetails(reviewPattern).get('pitchPattern')

    if reviewPattern.get("notePatternType") != "single_note_long_tone":
        direction = chooseDirection(pattern, reviewPattern.get('directions'))
        if direction == "descending":
            return descendingPattern(pattern)
        elif direction == "ascending descending":
            return ascendingDescendingPattern(pattern)
        elif direction == "descending ascending":
            return descendingAscendingPattern(pattern)
    return pattern


if __name__ == "__main__":
    app.run(debug=True)
