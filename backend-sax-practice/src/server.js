import express from 'express'
import {db, connectToDb } from './db.js'; 
import cors from 'cors'

const app = express();
const port = 8000
app.use(express.json())

app.use(cors({origin: "http://localhost:3000"}))

app.get('/api/programs/:programId', async (req,res) => {
  const { programId } = req.params;
  
  const program = await db.collection("programs").findOne({ programId })

  if (program){
    res.json(program);
  }else {
    res.sendStatus(404);
  };
});

app.get('/api/getExercises/', async (req,res) => { 
  try {
    const exercises = await db.collection("exercises").find().toArray();
    if (exercises){
      console.log(exercises)
      res.json(exercises);
    }else {
      res.sendStatus(404);
    }
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  } 
});

app.get('/api/getPrograms/', async (req,res) => { 
  try {
    const programs = await db.collection("programs").find().toArray();
    if (programs){
      console.log(programs)
      res.json(programs);
    }else {
      res.sendStatus(404);
    }
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  } 
});


app.put('/api/updateExerciseList/:studentName/', async (req, res) => {
  const { studentName } = req.params;
  const { currentExercise } = req.body;

  // Find the exercise by exerciseName
  let existingExercise = await db.collection("students").findOne({
    studentName,
    "exerciseList.exerciseName": currentExercise.title
  });

  if (existingExercise) {
    // Update the existing exercise
    let response = await db.collection("students").updateOne(
      {
        studentName,
        "exerciseList.exerciseName": currentExercise.title
      },
      {
        $inc: { "exerciseList.$.playCount": 1, "exerciseList.$.assessment": 1 }
      }
    );
    console.log(response);
  } else {
    // Exercise doesn't exist, insert a new exercise
    let assessmentUpdate = await db.collection("students").updateOne(
      { studentName },
      {
        $push: {
          "exerciseList": {
            "exerciseName": currentExercise.title,
            "playCount": 1,
            "assessment": 2
          }
        }
      },
      { upsert: true }
    );
    console.log(assessmentUpdate);
  }
});

app.put('/api/studentUpdate/:studentName', async (req, res) => {
  try{
    const{ studentName } = req.params;
    const{ student } = req.body;
    await db.collection("students").updateOne({ studentName },{
      $set: {"previousSet": student.previousSet,
            "program.currentIndex": student.program.currentIndex}
    })
    res.json({message: "Student Updated "});
  }catch(error){
    console.error("An error occured", error);
    res.status(500).send("Internal server error")
  };
});

// app.put('/api/studentPreviousSetUpdate/:studentName', async (req, res) => {
//   try{
//     const { studentName } = req.params;
//     const { exerciseSet } = req.body
//     await db.collection("students").updateOne({ studentName }, {
//       $set: {
//         previousSet: exerciseSet
//       }
//     });
//     res.send("Student updated")
//   } catch (error) {
//     console.error("An error occured", error);
//     res.status(500).send("Internal server error")
//   } 
// });

app.get('/api/students/:studentName', async (req, res) => {
  const { studentName } = req.params;
  const student = await db.collection("students").findOne({ studentName });
  if (student){
    res.json(student);
  }else{
    res.sendStatus(404);
  };  
});

connectToDb(() => {
  console.log("Connected to Database")
  app.listen(port, ()=> {
    console.log("Server is listening on port 8000");
});
})
