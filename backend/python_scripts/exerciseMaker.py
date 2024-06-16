from flask import Flask, request, jsonify
from flask_cors import CORS
from exerciseCollections.collectionCreator import collectionCreator
from queries.queries import (buildDatabase,
                             getCollections,
                             getPracticeSession,
                             logExerciseDetails,
                             fetchUserPrograms,
                             fetchModes,
                             fetchRhythmPatternOptions,
                             fetchUserExerciseLog,
                             fetchProgramData,
                             insertNewUserProgram)
from objects.PracticeSession import PracticeSession
import boto3

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
s3_client = boto3.client("s3")

@app.route("/")
def home():
    return "Connected"

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

@app.route("/userExerciseLog", methods=["GET", "POST"])
def userExerciseLog():
    try:
        sub = request.get_json().get('sub')
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

@app.route("/getRhythmPatternOptions", methods=["GET", "POST"])
def getRhythmPatternOptions():
    try:
        sub = request.get_json().get('sub')
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

@app.route("/getUserPrograms", methods=["GET", "POST"])
def getUserPrograms():
    try:
        sub = request.get_json().get('sub')
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

@app.route("/getProgramData", methods=["GET", "POST"])
def getProgramData():
    try:
        sub = request.get_json().get('sub')
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

@app.route("/getUserPracticeSession", methods=["GET", "POST"])
def getUserPracticeSession():
    try:
        sub = request.get_json().get('sub')
        practiceSession = getPracticeSession(sub)
        practiceSessionDict = practiceSession.toDict()
        return {
                "statusCode": 200,
                "practiceSession": practiceSessionDict
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

@app.route("/generateSet", methods=["GET", "POST"])
def generateSet():
    try:
        sub = request.get_json().get('sub')
        practiceSession = getPracticeSession(sub)
        practiceSession.createSession()
        return {
                "statusCode": 200,
                "sessionID": practiceSession.userPracticeSessionID,
                "rounds": practiceSession.rounds,
                "set": [exercise.toDict() for exercise in practiceSession.userPracticeSession]
        }

    except Exception as e:
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
