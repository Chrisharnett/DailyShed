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
