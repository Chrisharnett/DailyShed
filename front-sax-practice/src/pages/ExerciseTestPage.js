import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navigation from "../components/NavBar";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import axios from "axios";
import useUser from "../hooks/useUser";
import CurrentExercise from "../components/CurrentExercise";

const ExerciseTestPage = () => {
  const [currentExercise, setCurrentExercise] = useState({
    exerciseId: -1,
    exerciseFileName: "fronty",
    noteRhythmPattern: [
      [
        "repeat",
        [1, "4"],
        [2, "4"],
        [3, "4"],
        [4, "4"],
        [5, "4"],
        [6, "4"],
        [7, "4"],
        [8, "4"],
        [9, "4"],
        [8, "4"],
        [7, "4"],
        [6, "4"],
        [5, "4"],
        [4, "4"],
        [3, "4"],
        [2, "4"],
      ],
      [1, "1"],
    ],
    description: "Here's the description",
    key: "g",
    mode: "major",
    timeSignature: [4, 4],
    articulation: [],
    dynamics: [],
    preamble: "#(set-global-staff-size 14)",
  });
  const [exerciseURL, setExerciseURL] = useState(null);
IN PYTHON
//  To make a routine:
  // 1. Get the student
  // 2. Get the previous exerciseSet
  // 3. Get the current goal (notePattern collection).
  // 4. Get all rhythmPatterns.
  // 5. Find the next notePattern from the collection of exercises.
  // 6. If possible find a familiar rhythm for the new notePattern. If not, apply the next new rhythm to the notePattern.
  // 7. Apply new rhythms to the review exercises.
  // 8. For each exercise, check if it exists in bucket. If it does, get the URL. If not, create the exercise image.
  // 9. Start the routine. Update the student as they go.
  

  useEffect(() => {
    const getImage = async () => {
      try {
        let response = await axios.post(
          "/api/generateExercise",
          currentExercise
        );
        console.log("Image data received:", response.data);
        setExerciseURL(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getImage();
  }, [currentExercise]);

  if (exerciseURL) {
    return (
      <>
        <Navigation />
        <h1>Student Exercise Page</h1>
        <CurrentExercise exercise={currentExercise} src={exerciseURL} />
      </>
    );
  }
};

export default ExerciseTestPage;
