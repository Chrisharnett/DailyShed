import { Form, Container, Col, Row } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import AnimatedButton from "./common/AnimatedButton";

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

  const handleRemoveInterval = () => {
    removeInterval(i);
  };

  if (currentInterval) {
    return (
      <>
        <Container className="glass mb-2">
          <h3 className="fs-4">Exercise {i + 1}</h3>

          {/* Select Exercise Dropdown */}
          <Form.Group as={Row} className="mb-2 align-items-center">
            <Form.Label column sm="3" className="fw-bold">
              Select Exercise:
            </Form.Label>
            <Col sm="9">
              <Form.Select
                value={currentInterval.primaryCollection.primaryCollectionTitle}
                onChange={handleCollectionChange}
                id={i + "_collectionSelector"}
                className="glass-input"
              >
                {programs.map((program, index) => (
                  <option
                    key={i + "_" + index}
                    value={program.primaryCollection.primaryCollectionTitle}
                  >
                    {ToTitleCase(
                      program.primaryCollection.primaryCollectionTitle
                    )}
                  </option>
                ))}
              </Form.Select>
            </Col>
          </Form.Group>

          {/* Key, Rhythms, and Review Exercise Section */}
          <Row className="mb-3">
            <Col md={5} className="mb-3 mb-md-0">
              <div className="fw-bold">
                Key:{" "}
                <span className="">
                  {ToTitleCase(
                    currentInterval.tonic.tonicSequence[
                      currentInterval.tonic.scaleTonicIndex
                    ]
                  )}{" "}
                  {ToTitleCase(currentInterval.mode)}
                </span>
              </div>
            </Col>

            <Col md={5}>
              <div className="fw-bold">
                Rhythms:{" "}
                <span className="">
                  {ToTitleCase(
                    currentInterval.rhythmCollection.rhythmCollectionTitle
                  )}
                </span>
              </div>
            </Col>

            <Col md={2} className="d-flex align-items-center">
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

          {/* Remove Exercise Button */}
          <Row>
            <Col className="d-flex justify-content-end">
              <AnimatedButton
                variant="danger"
                className="mt-3"
                handleOnClick={handleRemoveInterval}
                buttonText={"Remove Exercise"}
              />
            </Col>
          </Row>
        </Container>
      </>
    );
  }
};

IntervalDetails.propTypes = {
  i: PropTypes.number,
  interval: PropTypes.object,
  programs: PropTypes.array,
  removeInterval: PropTypes.func,
  userPrograms: PropTypes.object,
  onDetailsChange: PropTypes.func,
  startAnimation: PropTypes.bool,
  cueNextAnimation: PropTypes.func,
};

export default IntervalDetails;
