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
        notes = stepwiseScaleNotePatterns(minNote, maxNote, (2 * maxNote))
        notes.extend(singleNoteLongToneWholeNotes(minNote, maxNote, (2 * maxNote)))
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


@app.route("/getSampleCollection", methods=["GET"])
def getSampleCollection():
    try:
        minNote = 1
        maxNote = 9
        notes = stepwiseScaleNotePatterns(minNote, maxNote, (2 * maxNote))
        rhythms = quarterNoteRhythms(4, 4)
        collection = Collection("Quarter Note Ninth Scale", notes, rhythms)

        return jsonify(collection)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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
        notes = stepwiseScaleNotePatterns(minNote, maxNote, (2 * maxNote))
        notes.extend(singleNoteLongToneWholeNotes(minNote, maxNote, (2 * maxNote)))
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


if __name__ == "__main__":
    app.run(debug=True)
