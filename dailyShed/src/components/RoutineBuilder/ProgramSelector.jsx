import PropTypes from "prop-types";
import { Card, Col, Row } from "react-bootstrap";
import { useEffect, useState, useContext } from "react";
import AddButton from "../common/AddButton";
import { RoutineContext } from "../../context/RoutineContext";

const ProgramSelector = () => {
  const [availablePrograms, setAvailablePrograms] = useState([]);

  const { routine } = useContext(RoutineContext);

  const handleSelectProgram = () => {};

  return (
    <Row>
      ProgramSelector
      <Col md={1}>
        <AddButton onClick={handleSelectProgram} />
      </Col>
    </Row>
  );
};

ProgramSelector.propTypes = {
  programs: PropTypes.array.isRequired,
};

export default ProgramSelector;
