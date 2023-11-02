from objects.exerciseObjects import Exercise
from flask import Flask, request, jsonify
from flask_cors import CORS
from objects.practiceSet import PracticeSet
from objects.player import Player
from objects.practiceSet import PracticeSet
from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns

app = Flask(__name__)

# cors = CORS(app, resources={r"/generate-exercise": {"origins": "*"}})


@app.route("/")
def home():
    return "Connected"

@app.route("/getManySets", methods=["GET", "POST"])
def getManySets():
    try:
        data = request.get_json()
        player = Player(
            currentStatus=data.currentStatus,
            exerciseHistory=data.exerciseHistory
        )
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
                returnSet.append({"exercise": exercise,
                                  "url": url})
            packageOfSets.append(returnSet)
        return packageOfSets
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/getSet", methods=["GET", "POST"])
def getSet():
    try:
        data = request.get_json()
        player = Player(data['previousSet'], data['currentStatus'], data['exerciseHistory'])
        minNote = 1
        maxNote = 9
        notes = notePatterns(minNote, maxNote, (2 * maxNote))
        rhythms = rhythmPatterns(4, 4)
        practiceSet = PracticeSet(player, notes, rhythms)
        currentSet = practiceSet.getNextSet()
        returnSet = []
        for exercise in currentSet:
            url = exercise.createImage()
            returnSet.append({"exercise": exercise.serialize(),
                              "url": url})
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
    app.run()
