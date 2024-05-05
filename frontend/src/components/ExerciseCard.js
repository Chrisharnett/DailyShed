import { Card, Button, Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import { SelfAssessmentModal } from "./SelfAssessmentModal";
import { SessionCompleteModal } from "./SessionComplete";

const ExerciseCard = ({
  exerciseCount,
  setExerciseCount,
  currentSet,
  setCurrentSet,
  buttonText,
  sessionID,
  setCreated,
  rounds,
}) => {
  const [showSelfAssementModal, setShowSelfAssessmentModal] = useState(false);
  const [currentSetIndex, setCurrentSetIndex] = useState(0);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [currentRound, setCurrentRound] = useState(1);
  const [showSessionCompleteModal, setShowSessionCompleteModal] =
    useState(false);
  const [imageURL, setImageURL] = useState(null);

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
    if (currentSetIndex === currentSet.length - 1) {
      advanceRound();
    }
    const nextSetIndex = exerciseCount % currentSet.length;
    setExerciseCount(exerciseCount + 1);
    setCurrentSetIndex(nextSetIndex);
  };

  useEffect(() => {
    setCurrentExercise(currentSet[currentSetIndex]);
    const filename = currentSet[currentSetIndex].filename;
    const url = filename + ".png";
    setImageURL(url);
  }, [currentRound, currentSet, currentSetIndex]);

  const nextExerciseHandler = () => {
    setShowSelfAssessmentModal(true);
  };

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
              <Card.Img variant="top" src={imageURL}></Card.Img>
              <Card.Text className="">{currentExercise.description}</Card.Text>
            </Card.Body>
          </Card>
          {currentRound <= rounds && (
            <Button type="submit" className="m-2" onClick={nextExerciseHandler}>
              {buttonText}
            </Button>
          )}
        </Container>
        <SelfAssessmentModal
          sessionID={sessionID}
          show={showSelfAssementModal}
          setShow={setShowSelfAssessmentModal}
          exercise={currentExercise}
          currentSet={currentSet}
          exerciseCount={exerciseCount}
          setShowSessionCompleteModal={setShowSessionCompleteModal}
          goToNextExercise={goToNextExercise}
        />
        <SessionCompleteModal
          show={showSessionCompleteModal}
          setShow={setShowSessionCompleteModal}
          currentSet={currentSet}
          setCreated={setCreated}
        />
      </>
    );
  }
};

export default ExerciseCard;
