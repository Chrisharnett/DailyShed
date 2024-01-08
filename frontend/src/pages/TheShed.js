import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import CurrentExercise from "../components/CurrentExercise";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect } from "react";
import axios from "axios";

const TheShed = () => {
  const [currentSet, setCurrentSet] = useState(null);
  const [currentSetIndex, setCurrentSetIndex] = useState(0);

  const user = useUser();

  useEffect(() => {
    const getSet = async () => {
      try {
        let response = await axios.post("/api/generateSet", user);
        console.log("Practice set data received:", response.data);
        setCurrentSet(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getSet();
  }, []);

  if (currentSet) {
    return (
      <>
        <Container>
          <h1>The Shed</h1>
          <h2>Exercise {currentSetIndex + 1}</h2>
          {<ExerciseCard exercise={currentSet[currentSetIndex]} />}
          <br></br>
          <br></br>
          <br></br>
        </Container>
      </>
    );
  }
};

export default TheShed;
