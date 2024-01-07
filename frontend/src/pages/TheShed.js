import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import CurrentExercise from "../components/CurrentExercise";
import { useState, useEffect } from "react";
import axios from "axios";

const TheShed = () => {
  const user = useUser();
  const { name } = user;
  const [currentSet, setCurrentSet] = useState(null);

  useEffect(() => {
    const getSet = async () => {
      try {
        let response = await axios.get("/api/generateSet");
        console.log("Practice set data received:", response.data);
        setCurrentSet(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getSet();
  }, []);

  return (
    <>
      <Container>
        <h1>The Shed</h1>
        <h2>{name}</h2>
        {/* <CurrentExercise /> */}
      </Container>
    </>
  );
};

export default TheShed;
