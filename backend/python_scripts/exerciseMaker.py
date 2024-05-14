from flask import Flask, request, jsonify
from flask_cors import CORS
from exerciseCollections.collectionCreator import collectionCreator
from setDesigner.queries import insertCollectionsInDatabase, insertPrograms, getCollections, getPracticeSession, logExerciseDetails, fetchUserPrograms, fetchModes
from practiceSession import PracticeSession
import boto3


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

s3_client = boto3.client("s3")

@app.route("/")
def home():
    return "Connected"

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

@app.route("/getUserPracticeSession", methods=["GET", "POST"])
def getUserPracticeSession():
    try:
        sub = request.get_json().get('sub')
        practiceSession = getPracticeSession(sub)
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

@app.route("/generateSet", methods=["GET", "POST"])
def generateSet():
    try:
        sub = request.get_json().get('sub')
        sessionData = getPracticeSession(sub)
        collections = getCollections(sessionData)
        practiceSession = PracticeSession(sessionData, collections)
        practiceSession.createSession()
        return {
                "statusCode": 200,
                "sessionID": practiceSession.userPracticeSessionID,
                "rounds": practiceSession.rounds,
                "set": practiceSession.userPracticeSession
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
        insertCollectionsInDatabase(collections)
        insertPrograms(programs)
        return {
                "statusCode": 200,
                "collections": collections}

    except Exception as e:
        return jsonify({
            "statusCode": 400,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)
