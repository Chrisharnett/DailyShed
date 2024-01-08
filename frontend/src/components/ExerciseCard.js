import { Card, Button, Modal } from "react-bootstrap";
import { useState } from "react";
import { SelfAssessmentModal } from "./SelfAssessmentModal";

const ExerciseCard = (props) => {
  const { exercise } = props;
  const [showSelfAssementModal, setShowSelfAssessmentModal] = useState(false);

  const nextExerciseHandler = () => {};

  return (
    <>
      <Card className="m-5 text-center blue-border">
        <Card.Body className="align-items-center">
          <Card.Title className="blue-header">
            {exercise.exerciseName}
          </Card.Title>
          <Card.Img variant="top" src={exercise.imageURL}></Card.Img>
          <Card.Text className="">{exercise.description}</Card.Text>
          <Button
            type="submit"
            className="mx-2"
            onClick={setShowSelfAssessmentModal}
          >
            Next Exercise
          </Button>
        </Card.Body>
      </Card>
      <SelfAssessmentModal
        show={showSelfAssementModal}
        setShow={setShowSelfAssessmentModal}
      />
    </>
  );
};

export default ExerciseCard;
