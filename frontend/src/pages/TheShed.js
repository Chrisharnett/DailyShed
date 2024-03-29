import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import TopSpacer from "../util/TopSpacer";

const TheShed = () => {
  const [currentSet, setCurrentSet] = useState(null);
  const [userData, setUserData] = useState(null);
  const [player, setPlayer] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [setLength, setSetLength] = useState(0);
  const [buttonText, setButtonText] = useState("Next Exercise");
  const hasCalledHandleNextSet = useRef(false);

  const user = useUser();

  useEffect(() => {
    if (currentSet && player) {
      if (exerciseCount === currentSet.length * player.program.rounds) {
        setButtonText("Complete!");
      } else {
        setButtonText("Next Exercise");
      }
    }
  }, [currentSet, exerciseCount, player]);

  useEffect(() => {
    if (user && !hasCalledHandleNextSet.current) {
      handleNextSet();
      hasCalledHandleNextSet.current = true;
    }
  }, [user]);

  const handleNextSet = async () => {
    try {
      let response = await axios.post(`/api/generateSet/${user.sub}`);
      const { set, player } = response.data;
      setCurrentSet(set);
      setPlayer(player);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  if (!currentSet) {
    return (
      <>
        <TopSpacer></TopSpacer>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Loading Practice Routine</h2>
          </div>
        </Container>
      </>
    );
  }
  // if (exerciseCount <= currentSet.length * player.program.rounds) {
  else {
    return (
      <>
        <TopSpacer></TopSpacer>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Practice Time</h2>
            <h3 className="dropShadow">
              Exercise {exerciseCount} of{" "}
              {currentSet.length * player.program.rounds}
            </h3>
          </div>
          <div className="d-flex flex-column align-items-center">
            {
              <ExerciseCard
                exerciseCount={exerciseCount}
                setExerciseCount={setExerciseCount}
                currentSet={currentSet}
                setCurrentSet={setCurrentSet}
                player={player}
                setPlayer={setPlayer}
                buttonText={buttonText}
              />
            }
          </div>
        </Container>
        <TopSpacer></TopSpacer>
      </>
    );

    // } else {
    //   return (
    //     <>
    //       <TopSpacer></TopSpacer>
    //       <Container
    //         className="d-flex align-items-center justify-content-center position-relative"
    //         style={{ height: "100vh", width: "100vw" }}
    //       >
    //         <Container
    //           className="midlayer glass"
    //           // onClick={handleNextSet}
    //           style={{ display: "inline-block", width: "auto" }}
    //         >
    //           <h1 className="dropShadow ">Routine Complete</h1>
    //         </Container>
    //       </Container>
    //       <TopSpacer></TopSpacer>
    //     </>
    //   );
  }
};

export default TheShed;
