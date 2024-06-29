import { Container, Card, Button } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";
import axios from "axios";

const ProgramCard = ({ i, user, program }) => {
  const [programLength, setProgramLength] = useState(0);

  useEffect(() => {}, []);

  const programTitle = () => {
    // const scalePatternType = program.programTitle.split(",")[1];
    const scalePatternType = program.programTitle;
    return (
      ToTitleCase(program.tonicSequence[program.scaleTonicIndex]) +
      " " +
      ToTitleCase(program.mode) +
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
