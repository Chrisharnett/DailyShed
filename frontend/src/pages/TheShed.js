import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import TopSpacer from "../util/TopSpacer";

const TheShed = () => {
  const [currentSet, setCurrentSet] = useState(null);
  const [userData, setUserData] = useState(null);
  const [exerciseCount, setExerciseCount] = useState(1);
  const [setLength, setSetLength] = useState(0);
  const [buttonText, setButtonText] = useState("Next Exercise");
  const hasCalledHandleNextSet = useRef(false);

  const user = useUser();

  useEffect(() => {
    if (currentSet && userData) {
      if (exerciseCount === currentSet.length * userData.program.rounds) {
        setButtonText("Complete!");
      } else {
        setButtonText("Next Exercise");
      }
    }
  }, [currentSet, exerciseCount, userData]);

  useEffect(() => {
    const getUserData = async () => {
      try {
        const response = await axios.get(`/api/getUserData/${user.sub}`);
        if (response.data.userData) {
          setUserData(response.data.userData);
          hasCalledHandleNextSet.current = false;
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
    if (userData && !hasCalledHandleNextSet.current) {
      handleNextSet();
      hasCalledHandleNextSet.current = true;
    }
  }, [userData]);

  const handleNextSet = async () => {
    if (!userData) {
      return;
    }
    try {
      let response = await axios.post("/api/generateSet", userData);
      const { player, returnSet } = response.data;
      setCurrentSet(returnSet);
      const { exerciseHistory, previousSet, program } = player;
      setUserData({
        ...userData,
        exerciseHistory: exerciseHistory,
        previousSet: previousSet,
        program: program,
      });
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
  if (exerciseCount <= currentSet.length * userData.program.rounds) {
    return (
      <>
        <TopSpacer></TopSpacer>
        <Container className="midLayer glass">
          <div className="titles p-2">
            <h2 className="dropShadow">Practice Time</h2>
            <h3 className="dropShadow">
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
                buttonText={buttonText}
              />
            }
          </div>
        </Container>
        <TopSpacer></TopSpacer>
      </>
    );
  } else {
    return (
      <>
        <TopSpacer></TopSpacer>
        <Container
          className="d-flex align-items-center justify-content-center position-relative"
          style={{ height: "100vh", width: "100vw" }}
        >
          <Container
            className="midlayer glass"
            // onClick={handleNextSet}
            style={{ display: "inline-block", width: "auto" }}
          >
            <h1 className="dropShadow ">Routine Complete</h1>
          </Container>
        </Container>
        <TopSpacer></TopSpacer>
      </>
    );
  }
};

export default TheShed;
