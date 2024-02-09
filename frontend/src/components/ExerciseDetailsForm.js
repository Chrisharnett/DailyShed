import { Form, Container, Row, Col } from "react-bootstrap";
import KeyAndModeSelector from "./KeyAndModeSelector";
import { useState } from "react";
import { useEffect } from "react";

const ExerciseDetailsForm = ({ i, details, collections, onDetailsChange }) => {
  const handleKeyChange = (key) => {
    onDetailsChange({ ...details, key });
  };

  const handleModeChange = (mode) => {
    onDetailsChange({ ...details, mode });
  };

  const handleCollectionChange = (e) => {
    onDetailsChange({ ...details, collectionName: e.target.value });
  };

  const handleCheckboxChange = (e) => {
    onDetailsChange({ ...details, reviewBool: e.target.checked });
  };

  useEffect(() => {
    onDetailsChange(details);
  }, [details]);

  return (
    <>
      <Container>
        <Row className="align-items-center">
          <Col xs={12} md={4} className="mb-2 mb-sm-0">
            <Form.Label>Exercise {i + 1}</Form.Label>
            <Form.Select
              value={details.collectionName}
              onChange={handleCollectionChange}
            >
              {collections.map((collection, index) => (
                <option key={index} value={collection.title}>
                  {collection.title}
                </option>
              ))}
            </Form.Select>
          </Col>
          <Col xs={12} md={5} className="mb-2 mb-sm-0">
            <KeyAndModeSelector
              keyCenter={details.key}
              mode={details.mode}
              onKeyChange={handleKeyChange}
              onModeChange={handleModeChange}
            />
          </Col>
          <Col xs={12} md={2} className="d-flex align-items-left">
            <Form.Check
              type="checkbox"
              label="Review Exercise"
              id={`reviewBool-${i}`}
              checked={details.reviewBool}
              onChange={handleCheckboxChange}
              className=""
            />
          </Col>
        </Row>
      </Container>
    </>
  );
};
export default ExerciseDetailsForm;
