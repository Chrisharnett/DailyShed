import { Row, Col, Form } from "react-bootstrap";
import { useState } from "react";
import ToTitleCase from "../util/ToTitleCase";

const KeyAndModeSelector = ({
  tonic,
  mode,
  tonicSequence,
  tonicSequenceName,
  scaleModes,
  onKeyChange,
  onModeChange,
  parentIndex,
}) => {
  // const [keys, setKeys] = useState([
  //   "c",
  //   "db",
  //   "d",
  //   "eb",
  //   "e",
  //   "f",
  //   "f#",
  //   "g",
  //   "g#",
  //   "a",
  //   "a#",
  //   "b",
  // ]);
  // const [scaleModes, setModes] = useState([
  //   "major",
  //   "minor",
  //   "dorian",
  //   "mixolydian",
  // ]);

  const handleKeyChange = (e) => {
    onKeyChange(e.target.value);
  };

  const handleModeChange = (e) => {
    onModeChange(e.target.value);
  };

  return (
    <>
      <Row>
        <Col xs={12} sm="auto">
          <Form.Group className="" controlId="keySelector">
            <Form.Label className="dropShadow fs-4">Key</Form.Label>
            <Form.Select value={tonic} onChange={handleKeyChange}>
              {tonicSequence.map((keyOption, i) => {
                const uniqueKey = `${parentIndex}_${keyOption}`;
                return (
                  <option key={uniqueKey} value={keyOption}>
                    {ToTitleCase(keyOption)}
                  </option>
                );
              })}
            </Form.Select>
            <Form.Text className="dropShadow fs-6">
              {tonicSequenceName}
            </Form.Text>
          </Form.Group>
        </Col>

        <Col xs={12} md="auto">
          <Form.Group className="" controlId="modeSelector">
            <Form.Label className="dropShadow fs-4">Mode</Form.Label>
            <Form.Select value={ToTitleCase(mode)} onChange={handleModeChange}>
              {scaleModes.map((modeOption, i) => (
                <option
                  key={`${parentIndex}_${modeOption}_${i}`}
                  value={modeOption}
                >
                  {ToTitleCase(modeOption)}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>
    </>
  );
};
export default KeyAndModeSelector;
