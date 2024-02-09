import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect } from "react";
import axios from "axios";

const TheShed = () => {
  const [currentSet, setCurrentSet] = useState(null);
  const [userData, setUserData] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);

  const user = useUser();

  useEffect(() => {
    const getUserData = async () => {
      try {
        const response = await axios.get(`/api/getUserData/${user.sub}`);
        if (response.data.userData) {
          setUserData(response.data.userData);
        } else {
          setUserData(null);
        }
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getUserData();
  }, [user]);

  useEffect(() => {
    const getSet = async () => {
      try {
        let response = await axios.post("/api/generateSet", userData);
        setCurrentSet(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (userData) {
      getSet();
    }
  }, [userData]);

  if (currentSet) {
    return (
      <>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2>Practice Time</h2>
            <h3>
              Exercise {exerciseCount} of{" "}
              {currentSet.length * userData.program.rounds}
            </h3>
          </div>
          <div className="d-flex flex-column align-items-center">
            {
              <ExerciseCard
                exerciseCount={exerciseCount}
                setExerciseCount={setExerciseCount}
                currentSet={currentSet}
                setCurrentSet={setCurrentSet}
                userData={userData}
                setUserData={setUserData}
              />
            }
          </div>
        </Container>
      </>
    );
  }
};

export default TheShed;
