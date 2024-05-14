import { Form, Container, Row, Col } from "react-bootstrap";
import KeyAndModeSelector from "./KeyAndModeSelector";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const ExerciseDetailsForm = ({
  i,
  interval,
  programs,
  scaleModes,
  onDetailsChange,
}) => {
  const [rhythmOptions, setRhythmOptions] = useState([]);

  useEffect(() => {
    // const rhythms = collections
    //   .filter(
    //     (collection) => collection.collectionTitle === details.collectionTitle
    //   )
    //   .map((collection) => collection.rhythmMatcher);
    // setRhythmOptions(rhythms);
  }, []);

  const handleKeyChange = (key) => {
    // onDetailsChange({ ...details, key });
  };

  const handleModeChange = (mode) => {
    // onDetailsChange({ ...details, mode });
  };

  const handleRhythmChange = (e) => {
    // onDetailsChange({ ...details, rhythmMatcher: e.target.value });
  };

  const handleCollectionChange = (e) => {
    // const matcher = collections.find(
    //   (collection) => collection.collectionTitle === e.target.value
    // ).notePatternType;
    // const rhythms = collections
    //   .filter((collection) => collection.collectionTitle === e.target.value)
    //   .flatMap((collection) => collection.rhythmMatcher);
    // if (rhythms.length > 0) {
    //   setRhythmOptions(rhythms);
    //   onDetailsChange({
    //     ...details,
    //     collectionTitle: e.target.value,
    //     notePatternType: matcher,
    //     rhythmMatcher: rhythms[0],
    //   });
    // } else {
    //   setRhythmOptions("None");
    //   onDetailsChange({
    //     ...details,
    //     collectionTitle: e.target.value,
    //     notePatternType: matcher,
    //     rhythmMatcher: null,
    //   });
    // }
  };

  const handleCheckboxChange = (e) => {
    // onDetailsChange({ ...details, reviewBool: e.target.checked });
  };

  // useEffect(() => {
  //   onDetailsChange(details);
  // }, [details]);

  return (
    <>
      <Container className="midlayer glass mb-3" style={{ width: "auto" }}>
        <Col xs={12} md="auto" className="my-2 fs-4">
          <Form.Label className="dropShadow">Exercise {i + 1}</Form.Label>
          <Form.Select
            value={ToTitleCase(interval.PrimaryCollectionTitle)}
            // onChange={handleCollectionChange}
          >
            {programs.map((program, index) => (
              <option key={index} value={program.programTitle}>
                {program.programTitle}
              </option>
            ))}
          </Form.Select>
        </Col>
        <KeyAndModeSelector
          keyCenter={interval.tonic}
          mode={interval.mode}
          modes={scaleModes}
          // onKeyChange={handleKeyChange}
          // onModeChange={handleModeChange}
          parentIndex={`${interval.collectionTitle}_${i}`}
        />
        <Col xs={12} md="auto" className="my-2 fs-4">
          <Form.Label className="dropShadow">Rhythm</Form.Label>
          <Form.Select
          // value={interval.rhythmMatcher}
          // onChange={handleRhythmChange}
          >
            {rhythmOptions.map((rhythm, index) => (
              <option key={index} value={rhythm}>
                {ToTitleCase(rhythm)}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col xs={12} md="auto" className="my-2 d-flex align-items-left fs-4">
          <Form.Check
            type="checkbox"
            label="Review Exercise"
            id={`reviewBool-${i}`}
            checked={interval.reviewBool}
            // onChange={handleCheckboxChange}
            className="dropShadow"
          />
        </Col>
      </Container>
    </>
  );
};
export default ExerciseDetailsForm;
