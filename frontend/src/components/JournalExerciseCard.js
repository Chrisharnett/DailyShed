import { Card } from "react-bootstrap";

const JournalExerciseCard = ({ exercise }) => {
  return (
    <>
      <Card className="journalExercise">
        <Card.Img variant="top" src={exercise.exercise.imageURL} />
      </Card>
    </>
  );
};

export default JournalExerciseCard;
