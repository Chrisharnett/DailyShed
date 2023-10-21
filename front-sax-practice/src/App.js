import "bootstrap/dist/css/bootstrap.min.css";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "./App.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ExSelection, ExerciseList } from "./components/exercise";
import Navigation from "./components/NavBar";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import axios from "axios";

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

export function Teacher() {
  const [exercises, setExercises] = useState(null);
  const [programs, setPrograms] = useState(null);
  const [newStudentName, setNewStudentName] = useState("");
  const [newStudentProgram, setNewStudentProgram] = useState([]);
  const [newProgramName, setNewProgramName] = useState("");
  const [newProgramGoal, setNewProgramGoal] = useState("");
  const [newProgramSequence, setNewProgramSequence] = useState([]);

  useEffect(() => {
    const getExercises = async () => {
      let response = await axios.get(`/api/getExercises`);
      setExercises(response.data);
    };
    getExercises();
  }, []);

  useEffect(() => {
    const getPrograms = async () => {
      let response = await axios.get(`/api/getPrograms`);
      setPrograms(response.data);
    };
    getPrograms();
  }, []);

  // TODO: Set number of rounds in student sign-in and teacher page.
  const handleCreateProgram = async () => {
    const exerciseSequence = [];
    for (let exercise of newProgramSequence) {
      for (let e of exercises) {
        if (
          e.patternId === exercise.patternId &&
          e.key === exercise.key &&
          e.mode === exercise.mode
        ) {
          exerciseSequence.push(e.exerciseId);
        }
      }
    }

    const newProgram = {
      programName: newProgramName,
      goal: newProgramGoal,
      exerciseSequence: exerciseSequence,
    };

    await axios.post(`/api/addNewProgram/`, {
      newProgram,
    });
  };

  const handleProgramSequenceChange = (newProgramSequence) => {
    setNewProgramSequence(newProgramSequence);
  };

  const handleNewStudent = async () => {
    if (newStudentName && newStudentProgram) {
      let newStudent = {
        studentName: newStudentName,
        program: {
          programId: 0,
          programName: newStudentProgram,
          currentIndex: 0,
        },
        exerciseList: [],
        previousSet: [],
      };
      let response = await axios.put(`/api/addStudent/`, { newStudent });
    }
  };

  if (exercises && programs)
    return (
      <div>
        <Navigation />
        <h1>Teacher Page</h1>
        <Container>
          <h2>Add New Student</h2>
          <Form>
            <Form.Control
              id="studentName"
              type="text"
              placeholder="Student Name"
              onChange={(e) => setNewStudentName(e.target.value)}
            ></Form.Control>
            <h3>Choose a student program</h3>
            <select
              id="newStudentProgramSelector"
              variant="success"
              title="Practice Programs"
              onChange={(e) => setNewStudentProgram(e.target.value)}
            >
              <option key={-1} id="" value={""}></option>
              {programs.map((program, index) => {
                return (
                  <option id={program.programId} key={index}>
                    {" "}
                    {program.programName}
                  </option>
                );
              })}
            </select>
            <Button variant="success" onClick={handleNewStudent}>
              Create Student
            </Button>
          </Form>
        </Container>
        <hr></hr>
        <Container>
          <h2>New Program Builder</h2>
          <p>
            Choose the exercises you would like in you program. Exercises are
            shown in G Major, but you can choose any key and mode in the
            dropdown menu.
          </p>
          <Container>
            <Form onSubmit={handleCreateProgram}>
              <Container></Container>
              <div className="inline">
                <input
                  type="text"
                  placeholder="Program Name"
                  value={newProgramName}
                  id="programName"
                  onChange={(e) => setNewProgramName(e.target.value)}
                ></input>
                <input
                  type="text"
                  placeholder="Program Goal"
                  id="programGoal"
                  value={newProgramGoal}
                  onChange={(e) => setNewProgramGoal(e.target.value)}
                ></input>
                <Button onClick={handleCreateProgram} variant="success">
                  Create Program
                </Button>
              </div>
              <div id="exerciseSelector">
                <ExSelection
                  exList={exercises}
                  onNewProgramSequenceChange={handleProgramSequenceChange}
                />
              </div>
            </Form>
          </Container>
        </Container>
      </div>
    );
}

export function Exercises() {
  const [exercises, setExercises] = useState(null);
  useEffect(() => {
    const getExercises = async () => {
      let response = await axios.get(`/api/getExercises`);
      setExercises(response.data);
    };
    getExercises();
  }, []);
  if (exercises)
    return (
      <div>
        <Navigation />
        <h1>Exercise List</h1>
        <ExerciseList exList={exercises} />
      </div>
    );
}

export function App() {
  return (
    <>
      <Navigation />
      <LoginPage />
      <HomePage />
    </>
  );
}
