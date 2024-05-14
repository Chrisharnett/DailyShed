import { Container, Card } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const ProgramCard = ({ i, program }) => {
  const [programLength, setProgramLength] = useState(0);

  useEffect(() => {}, []);

  return (
    <>
      <Container key={i}>
        <Card className="">
          <Card.Header>
            {program.programTitle} in{" "}
            {ToTitleCase(program.tonicSequence[program.scaleTonicIndex])}{" "}
            {ToTitleCase(program.mode)}
          </Card.Header>
          <Card.Body>
            <Card.Text>Instrument: {ToTitleCase(program.instrument)}</Card.Text>
            <Card.Text>
              Rhythm: {ToTitleCase(program.rhythmCollection)}
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
