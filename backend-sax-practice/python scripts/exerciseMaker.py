from flask import Flask, request, jsonify, Response
from exerciseObjects import Exercise
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/generate-exercise": {"origins": "*"}})


@app.route("/")
def home():
    return "Connected"


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
