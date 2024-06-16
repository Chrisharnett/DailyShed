import { Form, Container, Row, Col } from "react-bootstrap";
import KeyAndModeSelector from "./KeyAndModeSelector";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const ExerciseDetailsForm = ({
  i,
  interval,
  programs,
  scaleModes,
  rhythmOptions,
  onDetailsChange,
}) => {
  const [validRhythmOptions, setValidRhythmOptions] = useState([]);

  useEffect(() => {
    const validRhythms = rhythmOptions.filter(
      (rhythm) => rhythm.programTitle === interval.primaryCollectionTitle
    );
    setValidRhythmOptions(validRhythms);
  }, []);

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
            value={interval.primaryCollectionTitle}
            // onChange={handleCollectionChange}
          >
            {programs.map((program, index) => (
              <option key={index} value={program.programTitle}>
                {ToTitleCase(program.programTitle)}
              </option>
            ))}
          </Form.Select>
        </Col>
        <KeyAndModeSelector
          tonic={interval.tonic}
          mode={interval.mode}
          scaleModes={scaleModes}
          tonicSequence={interval.scaleTonicSequence}
          // onKeyChange={handleKeyChange}
          // onModeChange={handleModeChange}
          parentIndex={`${interval.primaryCollectionTitle}_${i}`}
        />
        <Col xs={12} md="auto" className="my-2 fs-4">
          <Form.Label className="dropShadow">Rhythm</Form.Label>
          <Form.Select
            value={ToTitleCase(interval.rhythmCollectionTitle)}
            // onChange={handleRhythmChange}
          >
            {validRhythmOptions.map((rhythm, index) => (
              <option key={index} value={rhythm.rhythmCollection}>
                {ToTitleCase(rhythm.rhythmCollection)}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col xs={12} md="auto" className="my-2 d-flex align-items-left fs-4">
          <Form.Check
            type="checkbox"
            label="Review Exercise"
            id={`reviewBool-${i}`}
            checked={interval.reviewExercise}
            // onChange={handleCheckboxChange}
            className="dropShadow"
          />
        </Col>
      </Container>
    </>
  );
};
export default ExerciseDetailsForm;
