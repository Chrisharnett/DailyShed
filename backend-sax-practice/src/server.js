import express from "express";
import { db, connectToDb } from "./db.js";
import "dotenv/config";

const app = express();
const port = 8000;
app.use(express.json());

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
      console.log(students);
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
      console.log(programs);
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

  // Find the exercise by exerciseName
  let existingExercise = await db.collection("students").findOne({
    studentName,
    "exerciseList.exerciseId": currentExercise.exerciseId,
  });

  if (existingExercise) {
    // Update the existing exercise
    let response = await db.collection("students").updateOne(
      {
        studentName,
        "exerciseList.exerciseId": currentExercise.exerciseId,
      },
      {
        $inc: { "exerciseList.$.playCount": 1, "exerciseList.$.assessment": 1 },
      }
    );
  } else {
    // Exercise doesn't exist, insert a new exercise
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
});

app.put("/api/studentUpdate/:studentName", async (req, res) => {
  try {
    const { studentName } = req.params;
    const { student } = req.body;
    await db.collection("students").updateOne(
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
    // res.send(`${newStudent.studentName} added.`);
  } catch (error) {
    console.error("Error adding program", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

connectToDb(() => {
  console.log("Connected to Database");
  app.listen(port, () => {
    console.log("Server is listening on port 8000");
  });
});
