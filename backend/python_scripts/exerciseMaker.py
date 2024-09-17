from flask import Flask, request, jsonify
from flask_cors import CORS
from exerciseCollections.collectionCreator import collectionCreator
from queries.queries import (
    updateUserSession,
    buildDatabase,
    getPracticeSession,
    logExerciseDetails,
    fetchUserPrograms,
    fetchModes,
    fetchRhythmPatternOptions,
    fetchUserExerciseLog,
    fetchProgramData,
    insertNewUserProgram,
    fetchUserPracticeSession
)
from util.exerciseBucket import checkTheBucketForImage
import boto3
import traceback

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
s3_client = boto3.client("s3")

@app.route("/")
def home():
    return "Connected"

#ACTIVE
@app.route("/addNewUserProgram", methods=["GET", "POST"])
def addNewUserProgram():
    try:
        details = request.get_json().get('program')
        userPrograms = insertNewUserProgram(details)
        return {
            "statusCode": 200,
            "userPrograms": userPrograms}

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/addNewUserSession", methods=["GET", "POST"])
def addNewUserSession():
    try:
        details = request.get_json().get('session')
        userPrograms = updateUserSession(details)
        return {
            "statusCode": 200,
            "userPrograms": userPrograms}

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/userExerciseLog/<sub>", methods=["GET", "POST"])
def userExerciseLog(sub):
    try:
        # sub = request.get_json().get('sub')
        history = fetchUserExerciseLog(sub)
        return {
                "statusCode": 200,
                "userHistory": history
        }
    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/getRhythmPatternOptions/<sub>", methods=["GET", "POST"])
def getRhythmPatternOptions(sub):
    try:
        # sub = request.get_json().get('sub')
        options = fetchRhythmPatternOptions(sub)
        return {
                "statusCode": 200,
                "rhythmPatternOptions": options
        }
    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/getScaleModes", methods=["GET"])
def getScaleModes():
    try:
        modes = fetchModes()
        return {
                "statusCode": 200,
                "modes": modes
        }

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

#ACTIVE
@app.route("/getUserPrograms/<sub>", methods=["GET", "POST"])
def getUserPrograms(sub):
    try:
        # sub = request.get_json().get('sub')
        programs = fetchUserPrograms(sub)
        return {
                "statusCode": 200,
                "programs": programs
        }

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

#ACTIVE
@app.route("/getProgramData/<sub>", methods=["GET", "POST"])
def getProgramData(sub):
    try:
        # sub = request.get_json().get('sub')
        programData = fetchProgramData(sub)
        return {
                "statusCode": 200,
                "programData": programData
        }

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

#ACTIVE
@app.route("/getUserPracticeSession/<sub>", methods=["GET", "POST"])
def getUserPracticeSession(sub):
    try:
        # sub = request.get_json().get('sub')
        practiceSession = fetchUserPracticeSession(sub)
        return {
                "statusCode": 200,
                "practiceSession": practiceSession
        }

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/logExercise", methods=["POST"])
def logExercise():
    try:
        details = request.get_json()
        logExerciseDetails(details)
        return {
            "statusCode": 200}

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/generateSet/<sub>", methods=["GET", "POST"])
def generateSet(sub):
    try:
        # sub = request.get_json().get('sub')
        practiceSession = getPracticeSession(sub)
        practiceSession.createSession()
        for interval in practiceSession.intervals:
            # Create the image if it doesn't exist
            if not checkTheBucketForImage(interval.filename):
                interval.createImage()
        return {
                "statusCode": 200,
                "sessionID": practiceSession.userPracticeSessionID,
                "rounds": practiceSession.rounds,
                "set": [exercise.toDict() for exercise in practiceSession.userPracticeSession]
        }

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

@app.route("/generateCollections", methods=["GET", "POST"])
def generateCollections():
    try:
        collections, programs = collectionCreator()
        buildDatabase(collections, programs)
        return {
                "statusCode": 200
        }

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)
