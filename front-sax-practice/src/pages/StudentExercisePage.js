import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CurrentExercise } from "../components/exercise";
import Navigation from "../components/NavBar";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import axios from "axios";
import useUser from "../auth/useUser";

const StudentExercisePage = () => {
  const { studentName } = useParams();
  const [student, setStudent] = useState(null);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [program, setProgram] = useState(null);
  const [thisSet, setThisSet] = useState(null);
  const [rounds, setRounds] = useState(2);
  // This is a feature I hope to implement later
  const [maxNew, setMaxNew] = useState(1);
  const [setLength, setSetLength] = useState(4);
  const [count, setCount] = useState(0);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [currentRound, setCurrentRound] = useState(0);
  const [exercises, setExercises] = useState(null);
  const [routineCompleted, setRoutineCompleted] = useState(false);

  // To access whether or not user is logged in
  const { user, isLoading } = useUser();

  // To use this (example pattern video)
  // {user
  //   ? show the user exercise routine
  //   : show a default exercise routine}

  // Load the current student & exercises
  useEffect(() => {
    const loadStudentInfo = async () => {
      const response = await axios.get(`/api/students/${studentName}`);
      setStudent(response.data);
    };
    loadStudentInfo();
  }, [studentName]);

  useEffect(() => {
    const getExercises = async () => {
      let response = await axios.get(`/api/getExercises`);
      setExercises(response.data);
    };
    getExercises();
  }, []);

  // Get the current program the student is studying.
  useEffect(() => {
    const getSetReady = async () => {
      if (student && exercises) {
        if (student.previousSet.length > 0) {
          setSetLength(student.previousSet.length);
        }

        if (student.program.programName === "") {
          //TODO: Temporary solution for a student with no program.
          student.program.programName = "G Major Scale 1";
        }
        const studentProgram = await axios.get(
          `/api/programs/${student.program.programName}`
        );
        setProgram(studentProgram.data);
      }
    };
    getSetReady();
  }, [student, exercises]);

  // Create a set for the student
  useEffect(() => {
    if (student && program) {
      let exerciseSet = [];
      let previousSet = student.previousSet;
      if (!previousSet || previousSet.length === 0) {
        for (let i = 0; i < setLength; i++) {
          exerciseSet.push(program.exerciseSequence[i]);
        }
        student.previousSet = exerciseSet;
        student.program.currentIndex = exerciseSet.length - 1;
      } else {
        // Start the new set with the previous set
        exerciseSet = student.previousSet;
        // Get the next Exercise
        let nextProgramExercise = "";
        if (
          student.program.currentIndex <
          program.exerciseSequence.length - 1
        ) {
          nextProgramExercise = getNextProgramExercise();
        } else {
          nextProgramExercise = getNextExercise();
        }

        // Replace the same patternType in the old exercise
        for (let i = 1; i < previousSet.length; i++) {
          if (
            exercises[previousSet[i]].patternType ===
              nextProgramExercise.patternType &&
            !exerciseSet.includes(nextProgramExercise)
          ) {
            exerciseSet[i] = nextProgramExercise.exerciseId;
          } else {
            // Choose appropriate review exercises for other exercises
            let reviewExercise = chooseReviewExercise(previousSet[i]);
            if (reviewExercise) {
              exerciseSet[i] = reviewExercise;
            } else {
              exerciseSet[i] = previousSet[i];
            }
          }
        }
      }
      setThisSet(exerciseSet);
      setCurrentExercise(exercises[exerciseSet[0]]);
      updateStudent();
    }
  }, [student, program, setLength]);

  const updateStudent = async () => {
    console.log("try to update student");
    let response = await axios.put(
      `/api/studentUpdate/${student.studentName}`,
      { student }
    );
  };

  const updateExercise = async () => {
    console.log("exercise update");
    const response = await axios.put(
      `/api/updateExerciseList/${student.studentName}`,
      { currentExercise }
    );
  };

  const handleNextExercise = async () => {
    console.log("handler");
    updateExercise();

    if (count < thisSet.length - 1) {
      setCount(count + 1);
      setExerciseCount(exerciseCount + 1);
      setCurrentExercise(exercises[thisSet[count + 1]]);
    } else {
      if (currentRound < rounds - 1) {
        setCurrentRound(currentRound + 1);
        shuffleSet();
        setCount(0);
        setCurrentExercise(exercises[thisSet[0]]);
        setExerciseCount(exerciseCount + 1);
      } else {
        setRoutineCompleted(true);
      }
    }
  };

  const chooseReviewExercise = (previousExercise) => {
    let m = Math.min(...student.exerciseList.map((ex) => ex.playCount));
    let possibleExercises = student.exerciseList
      .filter((x) => x.assessment <= m)
      .filter((x) => x.patternType === previousExercise.patternType);
    return (
      possibleExercises[
        Math.floor(Math.random() * possibleExercises.length) - 1
      ] || null
    );
  };

  const getNextProgramExercise = () => {
    student.program.currentIndex++;
    return program.exerciseSequence[student.program.currentIndex];
  };

  const getNextExercise = () => {
    const newExercise = exercises.find(
      (ex) => !student.exerciseList.some((e) => e.exerciseId === ex.exerciseId)
    );
    return newExercise || null;
  };

  // Fisher-Yates algorithm array shuffling algorithm.
  const shuffleSet = () => {
    let exercises = thisSet;
    for (let i = exercises.length - 1; i > 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));
      let temp = exercises[i];
      exercises[i] = exercises[j];
      exercises[j] = temp;
    }
    setThisSet(exercises);
  };

  if (currentExercise && !routineCompleted) {
    return (
      <>
        <Navigation />
        <h1>{student.studentName}</h1>
        <h2>{student.program.programName}</h2>
        <h3>
          Exercise {exerciseCount} of {setLength * rounds}
        </h3>
        <CurrentExercise exercise={currentExercise} />
        <button onClick={handleNextExercise} className="btn btn-primary">
          Next Exercise
        </button>
      </>
    );
  } else if (routineCompleted) {
    return (
      <div>
        <Navigation />
        <h1>Great job, today's routine is complete. See you next time!</h1>
      </div>
    );
  }
};

export function StudentSignIn() {
  const [studentList, setStudentList] = useState(null);
  const [currentStudent, setCurrentStudent] = useState(undefined);
  const navigate = useNavigate();

  useEffect(() => {
    const getStudents = async () => {
      let response = await axios.get(`/api/getStudents`);
      setStudentList(response.data);
    };
    getStudents();
  }, []);

  // TODO: Set number of rounds in student sign-in and teacher page.
  const handleStartRoutine = () => {
    let url = "/studentPracticePage/" + currentStudent;
    navigate(url);
  };

  const handleStudentChange = (event) => {
    setCurrentStudent(event.target.value);
  };
  if (studentList) {
    return (
      <div>
        <Navigation />
        <h1>Select student</h1>
        <select
          name="studentSelector"
          value={currentStudent}
          onChange={handleStudentChange}
        >
          <option key="n/a" />
          {studentList.map((student, index) => (
            <option key={student.studentName}>{student.studentName}</option>
          ))}
        </select>
        <Button
          onClick={() => {
            handleStartRoutine();
          }}
          variant="primary"
          className="m-2"
        >
          Start Routine
        </Button>
      </div>
    );
  }
}

export default StudentExercisePage;
