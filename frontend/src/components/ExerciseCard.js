import { Card, Button } from "react-bootstrap";
import { useState, useEffect } from "react";
import { SelfAssessmentModal } from "./SelfAssessmentModal";
import { SessionCompleteModal } from "./SessionComplete";

const ExerciseCard = ({
  exerciseCount,
  setExerciseCount,
  currentSet,
  setCurrentSet,
  userData,
  setUserData,
}) => {
  const [showSelfAssementModal, setShowSelfAssessmentModal] = useState(false);
  const [currentSetIndex, setCurrentSetIndex] = useState(0);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [currentRound, setCurrentRound] = useState(1);
  const [showSessionCompleteModal, setShowSessionCompleteModal] =
    useState(false);

  // Fisher-Yates algorithm array shuffling algorithm.
  const shuffleSet = () => {
    let newSet = [...currentSet];
    for (let i = newSet.length - 1; i > 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));
      let temp = newSet[i];
      newSet[i] = newSet[j];
      newSet[j] = temp;
    }
    setCurrentSet(newSet);
  };

  //Advance to the next round in a practice session
  const advanceRound = () => {
    let nextRound = currentRound + 1;
    setCurrentRound(nextRound);
    shuffleSet();
  };

  const goToNextExercise = () => {
    const nextSetIndex =
      exerciseCount % userData.program.exerciseDetails.length;
    setExerciseCount(exerciseCount + 1);
    setCurrentSetIndex(nextSetIndex);
  };

  useEffect(() => {
    setCurrentExercise(currentSet[currentSetIndex]);
    if (currentRound > userData.program.rounds) {
      setShowSessionCompleteModal(true);
    }
  }, [currentRound, currentSet, currentSetIndex, userData.program.rounds]);

  const nextExerciseHandler = () => {
    setShowSelfAssessmentModal(true);
    if (currentSetIndex === userData.program.exerciseDetails.length - 1) {
      advanceRound();
    }
    goToNextExercise();
  };

  if (currentExercise && currentRound <= userData.program.rounds) {
    return (
      <>
        <Card style={{ width: "50rem" }} className="m-5 text-center">
          <Card.Body className="align-items-center">
            <Card.Title className="">{currentExercise.exerciseName}</Card.Title>
            <Card.Img variant="top" src={currentExercise.imageURL}></Card.Img>
            <Card.Text className="">{currentExercise.description}</Card.Text>
            <Button
              type="submit"
              className="mx-2"
              onClick={nextExerciseHandler}
            >
              Next Exercise
            </Button>
          </Card.Body>
        </Card>
        <SelfAssessmentModal
          show={showSelfAssementModal}
          setShow={setShowSelfAssessmentModal}
          exercise={currentExercise}
          userData={userData}
          setUserData={setUserData}
        />
      </>
    );
  } else if (currentRound > userData.currentStatus.rounds) {
    return (
      <>
        <SessionCompleteModal
          show={showSessionCompleteModal}
          setShow={setShowSessionCompleteModal}
          currentSet={currentSet}
          userData={userData}
          setUserData={setUserData}
        />
      </>
    );
  }
};

export default ExerciseCard;
