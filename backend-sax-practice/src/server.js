// TEST COMMENT
import express from "express";
import { db, connectToDb } from "./db.js";
import "dotenv/config";
import path from "path";
import axios from "axios";
import https from "https";
import fs from "fs";
import { spawn } from "child_process";
import jwt from "jsonwebtoken";

import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 8000;

app.use(express.json());

// TODO: Is this approach acceptable for production??
app.use(express.static(path.join(__dirname, "../build")));

const venvPath = "./python scripts/exGenerator";

const pythonExecutable = path.join(venvPath, "bin/python");

const flaskServerScriptPath = path.join(
  __dirname,
  "../python scripts/exerciseMaker.py"
);

const flaskExerciseMaker = spawn(pythonExecutable, [flaskServerScriptPath]);

flaskExerciseMaker.stdout.on("data", (data) => {
  console.log(`Flask Server Output: ${data}`);
});

flaskExerciseMaker.stderr.on("data", (data) => {
  console.error(`Flask Server Error: ${data}`);
});

flaskExerciseMaker.on("close", (code) => {
  console.log(`Flask Server exited with code ${code}`);
});

app.get(/^(?!\/api).+/, (req, res) => {
  res.sendFile(path.join(__dirname, "../build/index.html"));
});

// Double Check this syntax from class video Nov. 3 ~ 20 minutes
app.get("/api/login", async (req, res) => {
  jwt.toString(
    { name: "Chris", accountID: 3 },
    process.env.JWT_SECRET,
    { exinresIn: "2d" },
    (err, token) => {
      if (err) {
        res.status(500).json(err);
      }

      res.status(200).json({ token });
    }
  );
});

app.post("/api/generateSet/", async (req, res) => {
  const exercise = req.body;
  // valid data: console.log(req.body);

  const exerciseMaker = "http://127.0.0.1:5000/getSet";

  try {
    const response = await axios.post(exerciseMaker, exercise, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status === 200) {
      res.status(200).json(response.data);
    } else {
      res.status(500).json({ error: "Image generation failed" });
    }
  } catch (error) {
    res.status(500).json({ error: "Error communicating with Flask server" });
  }
});

app.post("/api/addNewProgram/", async (req, res) => {
  const { newProgram } = req.body;
  try {
    let response = await db.collection("programs").insertOne(newProgram);
    res.status(201).json({ message: "Program added.", data: response.ops[0] });
  } catch (error) {
    console.error("Error adding program", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/api/programs/:programName", async (req, res) => {
  const { programName } = req.params;

  const program = await db.collection("programs").findOne({ programName });

  if (program) {
    res.json(program);
  } else {
    res.sendStatus(404);
  }
});

app.get("/api/getExercises/", async (req, res) => {
  try {
    const exercises = await db.collection("exercises").find().toArray();
    if (exercises) {
      res.json(exercises);
    } else {
      res.sendStatus(404);
    }
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  }
});

app.get("/api/getStudents", async (req, res) => {
  try {
    const students = await db.collection("students").find().toArray();
    if (students) {
      res.json(students);
    } else {
      res.sendStatus(404);
    }
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  }
});

app.get("/api/getPrograms/", async (req, res) => {
  try {
    const programs = await db.collection("programs").find().toArray();
    if (programs) {
      res.json(programs);
    } else {
      res.sendStatus(404);
    }
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  }
});

app.put("/api/updateExerciseList/:studentName/", async (req, res) => {
  const { studentName } = req.params;
  const { currentExercise } = req.body;

  try {
    let existingExercise = await db.collection("students").findOne({
      studentName,
      "exerciseList.exerciseId": currentExercise.exerciseId,
    });
    res.json({ message: "Exercise Found " });
    if (existingExercise) {
      console.log("exercise exists");
      let response = await db.collection("students").updateOne(
        {
          studentName,
          "exerciseList.exerciseId": currentExercise.exerciseId,
        },
        {
          $inc: {
            "exerciseList.$.playCount": 1,
            "exerciseList.$.assessment": 1,
          },
        }
      );
      console.log(
        `exerciseList updated with ${currentExercise.exerciseName} for ${studentName}`
      );
    } else {
      // Exercise doesn't exist, insert a new exercise
      console.log("exercise is new");
      let assessmentUpdate = await db.collection("students").updateOne(
        { studentName },
        {
          $push: {
            exerciseList: {
              exerciseId: currentExercise.exerciseId,
              playCount: 1,
              assessment: 2,
            },
          },
        },
        { upsert: true }
      );
    }
  } catch (error) {
    console.error("An error occured", error);
    res.status(500).send("Internal server error");
  }
});

app.put("/api/studentUpdate/:studentName", async (req, res) => {
  try {
    const { studentName } = req.params;
    const { student } = req.body;
    let response = await db.collection("students").updateOne(
      { studentName },
      {
        $set: {
          previousSet: student.previousSet,
          "program.currentIndex": student.program.currentIndex,
        },
      }
    );
    res.json({ message: "Student Updated " });
  } catch (error) {
    console.error("An error occured", error);
    res.status(500).send("Internal server error");
  }
});

app.get("/api/students/:studentName", async (req, res) => {
  const { studentName } = req.params;
  const student = await db.collection("students").findOne({ studentName });
  if (student) {
    res.json(student);
  } else {
    res.sendStatus(404);
  }
});

app.put("/api/addStudent/", async (req, res) => {
  try {
    const { newStudent } = req.body;

    await db.collection("students").insertOne(newStudent);
  } catch (error) {
    console.error("Error adding program", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/api/replacePrograms/", async (req, res) => {
  if (req.body.apiKey === process.env.API_KEY) {
    try {
      await db.collection("programs").deleteMany({});
      await db.collection("programs").insertMany(req.body.programs);
      res.json("Programs replaced");
    } catch (error) {
      res.error("Internal Server Error", error);
    }
  }
});

connectToDb(() => {
  console.log("Connected to Database");
  app.listen(port, () => {
    console.log("Server is listening on port 8000");
  });
});
