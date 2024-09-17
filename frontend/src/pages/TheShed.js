import Container from "react-bootstrap/Container";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect, useRef } from "react";
import { setGenerator } from "../util/flaskRoutes";
import axios from "axios";

const TheShed = ({ user }) => {
  const [currentSet, setCurrentSet] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [buttonText, setButtonText] = useState("Next Exercise");
  const [sessionID, setSessionID] = useState(null);
  const setCreated = useRef(false);
  const [rounds, setRounds] = useState(1);

  useEffect(() => {
    if (currentSet) {
      if (exerciseCount === currentSet.length) {
        setButtonText("Complete!");
      } else {
        setButtonText("Next Exercise");
      }
    }
  }, [currentSet, exerciseCount]);

  useEffect(() => {
    const handleNextPracticeSession = async () => {
      try {
        const response = await axios.post(`${setGenerator}/${user.sub}`);
        const sessionData = response.data;
        setSessionID(sessionData.sessionID);
        setCurrentSet(sessionData.set);
        setRounds(sessionData.rounds);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (!setCreated.current && user) {
      setCreated.current = true;
      handleNextPracticeSession();
    }
  }, [user]);

  if (!currentSet) {
    return (
      <>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Loading Practice Routine</h2>
          </div>
        </Container>
      </>
    );
  } else {
    return (
      <>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Practice Time</h2>
            <h3 className="dropShadow">
              Exercise {exerciseCount} of {currentSet.length * rounds}
            </h3>
          </div>
          <div className="d-flex flex-column align-items-center">
            {
              <ExerciseCard
                sessionID={sessionID}
                exerciseCount={exerciseCount}
                setExerciseCount={setExerciseCount}
                currentSet={currentSet}
                setCurrentSet={setCurrentSet}
                buttonText={buttonText}
                setCreated={setCreated}
                rounds={rounds}
                user={user}
              />
            }
          </div>
        </Container>
      </>
    );
  }
};

export default TheShed;
