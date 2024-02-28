import { Card, Button, Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import { SelfAssessmentModal } from "./SelfAssessmentModal";
import { SessionCompleteModal } from "./SessionComplete";

const ExerciseCard = ({
  exerciseCount,
  setExerciseCount,
  currentSet,
  setCurrentSet,
  player,
  setPlayer,
  buttonText,
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
    const nextSetIndex = exerciseCount % player.program.exerciseDetails.length;
    setExerciseCount(exerciseCount + 1);
    setCurrentSetIndex(nextSetIndex);
  };

  useEffect(() => {
    setCurrentExercise(currentSet[currentSetIndex]);
  }, [currentRound, currentSet, currentSetIndex]);

  const nextExerciseHandler = () => {
    setShowSelfAssessmentModal(true);
    if (currentSetIndex === player.program.exerciseDetails.length - 1) {
      advanceRound();
    }
    goToNextExercise();
  };

  // if (currentExercise && currentRound <= player.program.rounds) {
  if (currentExercise) {
    return (
      <>
        <Container className="cardContainer d-flex flex-column align-items-center">
          <Card border="light" className="exerciseCard ">
            <Card.Body className="align-items-center">
              <Card.Title className="">
                {currentExercise.collectionTitle}
              </Card.Title>
              <Card.Title className="">
                {currentExercise.exerciseName}
              </Card.Title>
              <Card.Img variant="top" src={currentExercise.imageURL}></Card.Img>
              <Card.Text className="">{currentExercise.description}</Card.Text>
            </Card.Body>
          </Card>
          {currentRound <= player.program.rounds && (
            <Button type="submit" className="m-2" onClick={nextExerciseHandler}>
              {buttonText}
            </Button>
          )}
        </Container>
        <SelfAssessmentModal
          show={showSelfAssementModal}
          setShow={setShowSelfAssessmentModal}
          exercise={currentExercise}
          currentSet={currentSet}
          player={player}
          setPlayer={setPlayer}
          exerciseCount={exerciseCount}
          setShowSessionCompleteModal={setShowSessionCompleteModal}
        />
        <SessionCompleteModal
          show={showSessionCompleteModal}
          setShow={setShowSessionCompleteModal}
          currentSet={currentSet}
          player={player}
          setPlayer={setPlayer}
        />
      </>
    );
  }
};

export default ExerciseCard;
