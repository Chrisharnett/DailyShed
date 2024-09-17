import { Form, Container, Col, Button, Row } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const IntervalDetails = ({
  i,
  interval,
  programs,
  removeInterval,
  userPrograms,
  onDetailsChange,
}) => {
  const [currentInterval, setCurrentInterval] = useState(null);

  useEffect(() => {
    const intervalDetails = programs.find(
      (program) => program.programID === interval.programID
    );
    setCurrentInterval(intervalDetails);
  }, [interval.programID, programs]);

  const handleCollectionChange = (e) => {
    const newProgram = programs[e.target.selectedIndex];
    const newUserProgram = userPrograms.programs.find(
      (program) => program.programID === newProgram.programID
    );
    const newIntervalData = {
      currentIndex: newProgram.currentIndex,
      primaryCollectionId: newProgram.primaryCollection.primaryCollectionID,
      programID: newProgram.programID,
      rhythmCollectionID: newProgram.rhythmCollection.rhythmCollectionID,
      scaleTonicIndex: newProgram.tonic.scaleTonicIndex,
      userProgramID: newUserProgram.userProgramID,
    };

    onDetailsChange({ ...interval, ...newIntervalData });
  };

  const handleCheckboxChange = (e) => {
    onDetailsChange({ ...interval, reviewExercise: e.target.checked });
  };

  const handleRemoveInterval = (e) => {
    removeInterval(i);
  };

  if (currentInterval) {
    return (
      <>
        <Container className="midlayer glass mb-3" style={{ width: "100%" }}>
          <Col xs={12} md="auto" className="my-2 fs-4">
            <h2>Exercise {i + 1}</h2>
            <Form.Label>Your Programs</Form.Label>
            <Form.Select
              value={currentInterval.primaryCollection.primaryCollectionTitle}
              onChange={handleCollectionChange}
              id={i + "_collectionSelector"}
            >
              {programs.map((program, index) => (
                <option
                  key={i + "_" + index}
                  value={program.primaryCollection.primaryCollectionTitle}
                  data-index={program.programID}
                >
                  {ToTitleCase(
                    program.primaryCollection.primaryCollectionTitle
                  )}
                </option>
              ))}
            </Form.Select>
          </Col>

          <Row>
            <Col xs={4}>
              <h3>Current Key</h3>
              {ToTitleCase(
                currentInterval.tonic.tonicSequence[
                  currentInterval.tonic.scaleTonicIndex
                ]
              )}{" "}
              {ToTitleCase(currentInterval.mode)}
            </Col>
            <Col xs={4}>
              <h3>Rhythms</h3>
              {ToTitleCase(
                currentInterval.rhythmCollection.rhythmCollectionTitle
              )}
            </Col>
            <Col xs={4} md="auto" className="my-2 d-flex align-items-left fs-4">
              <Form.Check
                type="checkbox"
                label="Review Exercise"
                id={`reviewBool-${i}`}
                checked={interval.reviewExercise}
                onChange={handleCheckboxChange}
                className="dropShadow"
              />
            </Col>
          </Row>
          <Row>
            <Col xs={6}>
              <Button
                variant="warning"
                className="m-3"
                onClick={handleRemoveInterval}
              >
                Remove
              </Button>
            </Col>
          </Row>
        </Container>
      </>
    );
  }
};
export default IntervalDetails;
