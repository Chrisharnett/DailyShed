import { Container, Row, Col, Form } from "react-bootstrap";
import { useEffect, useState } from "react";
import axios from "axios";

const KeyAndModeSelector = ({ keyCenter, mode, onKeyChange, onModeChange }) => {
  const [keys, setKeys] = useState(["c", "d", "e", "f", "g", "a", "b"]);
  const [modes, setModes] = useState([
    "major",
    "minor",
    "dorian",
    "mixolydian",
  ]);

  const handleKeyChange = (e) => {
    onKeyChange(e.target.value);
  };

  const handleModeChange = (e) => {
    onModeChange(e.target.value);
  };

  return (
    <>
      <Container>
        <Row>
          <Col xs={12} md={3}>
            <Form.Group className="mb-3" controlId="keySelector">
              <Form.Label
                style={{
                  color: "rgb(255, 255, 255)",
                  textShadow: "3px 2px 2px rgba(0, 0, 0, 0.8)",
                }}
              >
                Key
              </Form.Label>
              <Form.Select value={keyCenter} onChange={handleKeyChange}>
                {keys.map((keyOption, i) => {
                  return (
                    <option key={i} value={keyOption}>
                      {keyOption}
                    </option>
                  );
                })}
              </Form.Select>
            </Form.Group>
          </Col>

          <Col xs={12} md={4}>
            <Form.Group className="mb-3" controlId="modeSelector">
              <Form.Label
                style={{
                  color: "rgb(255, 255, 255)",
                  textShadow: "3px 2px 2px rgba(0, 0, 0, 0.8)",
                }}
              >
                Mode
              </Form.Label>
              <Form.Select value={mode} onChange={handleModeChange}>
                {modes.map((modeOption, index) => (
                  <option key={index} value={modeOption}>
                    {modeOption}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>
      </Container>
    </>
  );
};
export default KeyAndModeSelector;
