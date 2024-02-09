# import debugpy
from objects.exerciseObjects import Exercise
from flask import Flask, request, jsonify
from flask_cors import CORS
from objects.player import Player
from objects.practiceSet import PracticeSet
from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
import boto3

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
        data = request.get_json()
        player = Player(program=data.program, exerciseHistory=data.exerciseHistory)
        numberOfSets = 20
        minNote = 1
        maxNote = 9
        notes = notePatterns(minNote, maxNote, (2 * maxNote))
        rhythms = rhythmPatterns(4, 4)
        packageOfSets = []
        for i in range(numberOfSets):
            practiceSet = PracticeSet(player, notes, rhythms)
            returnSet = []
            for exercise in practiceSet:
                url = exercise.createImage()
                returnSet.append({"exercise": exercise, "url": url})
            packageOfSets.append(returnSet)
        return packageOfSets
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/getSampleCollection", methods=["GET"])
def getSampleCollection():
    try:
        minNote = 1
        maxNote = 9
        collections = []
        notes = notePatterns(minNote, maxNote, (2 * maxNote))
        for n in notes:
            collections.append(n.serialize())
        return jsonify(collections)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/getCollections", methods=["GET"])
def getCollections():
    try:
        minNote = 1
        maxNote = 9
        collections = []
        notes = notePatterns(minNote, maxNote, (2 * maxNote))
        for n in notes:
            collections.append(n.serialize())
        return jsonify(collections)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/getSet", methods=["GET", "POST"])
def getSet():
    try:
        bucketName = "mysaxpracticeexercisebucket"
        print(bucketName)
        data = request.get_json()
        player = Player(data["previousSet"], data["program"], data["exerciseHistory"])
        minNote = 1
        maxNote = 9
        notes = notePatterns(minNote, maxNote, (2 * maxNote))
        rhythms = rhythmPatterns(4, 4)
        practiceSet = PracticeSet(player, notes, rhythms)
        currentSet = practiceSet.getNextSet()
        returnSet = []

        for exercise in currentSet:
            try:
                objectKey = exercise.exerciseFileName()
                s3_client.head_object(Bucket=bucketName, Key=objectKey)
            except Exception as e:
                exercise.createImage()
            e = exercise.serialize()
            url = exercise.imageURL()
            returnSet.append(e)
        return returnSet
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/generateExercise", methods=["POST"])
def generateExercise():
    try:
        data = request.get_json()
        exercise = Exercise(
            data["exerciseId"],
            data["exerciseFileName"],
            data["noteRhythmPattern"],
            data["description"],
            data["key"],
            data["mode"],
            data["timeSignature"],
            data["articulation"],
            data["dynamics"],
            data["preamble"],
        )

        return exercise.createImage()

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
