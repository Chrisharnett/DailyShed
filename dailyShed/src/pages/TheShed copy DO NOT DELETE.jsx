import Container from "react-bootstrap/Container";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect, useRef } from "react";
import { setGenerator } from "../util/flaskRoutes";
import axios from "axios";
import { useUserContext } from "../auth/useUserContext";
import LoadingScreen from "../components/common/LoadingScreen";
import GlassContainer from "../components/common/GlassContainer";

const TheShed = () => {
  const [currentSet, setCurrentSet] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [buttonText, setButtonText] = useState("Next Exercise");
  const [sessionID, setSessionID] = useState(null);
  const [cueExerciseCard, setCueExerciseCard] = useState(false);
  const setCreated = useRef(false);
  const [rounds, setRounds] = useState(1);
  const { user } = useUserContext();

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
    return <LoadingScreen message="Loading Practice Routine" />;
  } else {
    return (
      <>
        <GlassContainer
          title="Practice Time"
          subtitle={`Exercise ${exerciseCount} of ${
            currentSet.length * rounds
          }`}
          startAnimation={true}
          cueNextAnimation={setCueExerciseCard}
        >
          <Container className="d-flex flex-column align-items-center">
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
                startAnimation={cueExerciseCard}
              />
            }
          </Container>
        </GlassContainer>
      </>
    );
  }
};

export default TheShed;
