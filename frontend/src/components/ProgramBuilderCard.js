import { Container, Card, Form } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";
import KeyAndModeSelector from "./KeyAndModeSelector";

// A program has scaleMode, rhythmCollection, primaryCollection, tonicSequence, instrument.

const ProgramBuilderCard = (
  tonic,
  mode,
  scaleTonicSequence,
  tonicSequenceName,
  scaleModes,
  onKeyChange,
  onModeChange,
  parentIndex
) => {
  useEffect(() => {}, []);

  return (
    <>
      <Container>
        <Card className="">
          <Card.Header>Title</Card.Header>
          <Card.Body>
            <Card.Text>Starting Key: {}</Card.Text>

            <Card.Text>
              <KeyAndModeSelector
                tonic={tonic}
                mode={mode}
                scaleTonicSequence={scaleTonicSequence}
                tonicSequenceName={tonicSequenceName}
                scaleModes={scaleModes}
                onKeyChange={onKeyChange}
                onModeChange={onModeChange}
                parentIndex={parentIndex}
              />
            </Card.Text>
            <Form.Select
            // value={}
            // onChange={handleCollectionChange}
            >
              {/* {programs.map((program, index) => (
                <option
                  key={index}
                  // value={}
                >
                  {ToTitleCase()}
                </option>
              ))} */}
            </Form.Select>
            <Card.Text>Instrument: {}</Card.Text>
            <Card.Text>Rhythm: {}</Card.Text>
            <Card.Text>Key Sequence: {}</Card.Text>
          </Card.Body>
          <Card.Footer></Card.Footer>
        </Card>
      </Container>
    </>
  );
};
export default ProgramBuilderCard;
