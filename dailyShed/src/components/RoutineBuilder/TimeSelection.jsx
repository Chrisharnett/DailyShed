import PropTypes from "prop-types";
import AnimatedButton from "../common/AnimatedButton";
import { useEffect, useState } from "react";
import { Container } from "react-bootstrap";

const TimeSelection = ({ onNext, setSubtitle }) => {
  const [customTime, setCustomTime] = useState("");

  useEffect(() => {
    setSubtitle("How long will you spend in the shed?");
  }, [setSubtitle]);

  const handleTimeSelect = (time) => {
    if (isNaN(time) || time <= 0) {
      alert("Please enter a valid time in minutes.");
      return;
    }
    onNext(time);
  };

  const defaultTimes = [
    { value: 15, text: "15 minutes" },
    { value: 30, text: "30 minutes" },
    { value: 45, text: "45 minutes" },
    { value: 60, text: "1 hour" },
  ];

  return (
    <>
      <Container
        fluid
        className="d-flex justify-content-between align-items-center"
      >
        {defaultTimes.map((time, index) => (
          <AnimatedButton
            key={index}
            handleOnClick={() => handleTimeSelect(time.value)}
            buttonText={time.text}
          />
        ))}
      </Container>
      <hr />
      <Container fluid className="d-flex  align-items-left">
        {" "}
        <input
          type="number"
          min="1"
          placeholder="In minutes"
          value={customTime}
          onChange={(e) => setCustomTime(e.target.value)}
          className="form-control"
          style={{ width: "150px" }}
        />
        <AnimatedButton
          handleOnClick={() => handleTimeSelect(parseInt(customTime))}
          buttonText="Set Custom Time"
          className="mt-2"
        />
      </Container>
    </>
  );
};

TimeSelection.propTypes = {
  onNext: PropTypes.func.isRequired,
  setSubtitle: PropTypes.func.isRequired,
};

export default TimeSelection;
