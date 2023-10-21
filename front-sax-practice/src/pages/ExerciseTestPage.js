import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navigation from "../components/NavBar";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import axios from "axios";
import useUser from "../hooks/useUser";
import CurrentExercise from "../components/CurrentExercise";

const ExerciseTestPage = () => {
  const [imageData, setImageData] = useState(null);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [exerciseURL, setExerciseURL] = useState(null);

  setCurrentExercise({
    exerciseId: -1,
    exerciseURL: "NA",
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
    })

  useEffect(() => {
    await axios
      .post("/api/generateExercise", currentExercise)
      .then((response) => {
        console.log("Image data received:", response.data);
        setExercise(response.data.image);
      })
      .catch((error) => {
        console.error("Error: ", error);
      });

    return (
      <>
        <Navigation />
        <h1>Student Exercise Page</h1>
        <CurrentExercise exercise={currentExercise} src={exerciseURL} />
      </>
    );
  });
};

export default ExerciseTestPage;
