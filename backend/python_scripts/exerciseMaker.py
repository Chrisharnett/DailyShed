from flask import Flask, request, jsonify
from flask_cors import CORS
from objects.player import Player
from objects.practiceSet import PracticeSet
from notePatternGenerator import stepwiseScaleNotePatterns, singleNoteLongToneWholeNotes
from rhythmPatternGenerator import quarterNoteRhythms, singleNoteWholeToneRhythms
from setDesigner.setDesigner import setDesigner
from setDesigner.getPlayer import getPlayerData
from util import getPlayer
import boto3

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

s3_client = boto3.client("s3")

@app.route("/")
def home():
    return "Connected"

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

@app.route("/generateSet", methods=["GET", "POST"])
def generateSet():
    try:
        data = request.get_json()
        userSub = data.get('sub')
        player = getPlayerData(userSub)
        newPracticeSet, player = setDesigner(player)
        return {
                "statusCode": 200,
                "set": newPracticeSet,
                "player": player}

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)
