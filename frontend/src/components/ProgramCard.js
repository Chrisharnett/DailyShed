import { Container, Card } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const ProgramCard = ({ i, program }) => {
  const [programLength, setProgramLength] = useState(0);

  useEffect(() => {}, []);

  const programTitle = () => {
    const scalePatternType = program.collectionTitle.split(",")[1];
    return (
      ToTitleCase(program.sequence[program.scaleTonicIndex]) +
      " " +
      ToTitleCase(program.scaleModeName) +
      " " +
      scalePatternType
    );
  };

  return (
    <>
      <Container key={i}>
        <Card className="">
          <Card.Header>{programTitle()}</Card.Header>
          <Card.Body>
            <Card.Text>
              Instrument: {ToTitleCase(program.instrumentName)}
            </Card.Text>
            <Card.Text>Level: {ToTitleCase(program.instrumentLevel)}</Card.Text>
            <Card.Text>
              Rhythm: {ToTitleCase(program.rhythmCollection)}
            </Card.Text>
            <Card.Text>
              Key Sequence: {ToTitleCase(program.tonicSequenceName)}
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            Exercises completed: {program.currentIndex + 1} of{" "}
            {program.collectionLength}
          </Card.Footer>
        </Card>
      </Container>
    </>
  );
};
export default ProgramCard;
