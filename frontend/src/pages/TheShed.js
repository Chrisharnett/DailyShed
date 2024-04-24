import Container from "react-bootstrap/Container";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import TopSpacer from "../util/TopSpacer";
import { v4 as uuidV4 } from "uuid";

const TheShed = ({ user, playerDetails, updatePlayerDetails }) => {
  const [currentSet, setCurrentSet] = useState(null);
  // const [player, setPlayer] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [buttonText, setButtonText] = useState("Next Exercise");
  // const hasCalledHandleNextSet = useRef(false);
  const [sessionID, setSessionID] = useState(null);
  const setCreated = useRef(false);

  useEffect(() => {
    const ID = uuidV4();
    setSessionID(ID);
  }, []);

  useEffect(() => {
    if (currentSet && playerDetails) {
      if (exerciseCount === currentSet.length * playerDetails.program.rounds) {
        setButtonText("Complete!");
      } else {
        setButtonText("Next Exercise");
      }
    }
  }, [currentSet, exerciseCount, playerDetails]);

  // useEffect(() => {
  //   if (user && !hasCalledHandleNextSet.current) {
  //     handleNextSet();
  //     hasCalledHandleNextSet.current = true;
  //   }
  // }, [user]);

  useEffect(() => {
    const handleNextSet = async () => {
      try {
        let response = await axios.post(
          `/api/generateSet/${user.sub}`,
          playerDetails
        );
        const { set, player } = response.data;
        setCurrentSet(set);
        updatePlayerDetails(player);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (playerDetails && !setCreated.current) {
      setCreated.current = true;
      handleNextSet();
    }
  }, [user, playerDetails]);

  if (!currentSet) {
    return (
      <>
        <TopSpacer />
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
        <TopSpacer />
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Practice Time</h2>
            <h3 className="dropShadow">
              Exercise {exerciseCount} of{" "}
              {currentSet.length * playerDetails.program.rounds}
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
                playerDetails={playerDetails}
                updatePlayerDetails={updatePlayerDetails}
                buttonText={buttonText}
                setCreated={setCreated}
              />
            }
          </div>
        </Container>
        <TopSpacer />
      </>
    );
  }
};

export default TheShed;
