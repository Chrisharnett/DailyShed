import PropTypes from "prop-types";
import { Card, Col, Row } from "react-bootstrap";
import { useEffect, useState } from "react";
import AddButton from "../common/AddButton";
import ProgramCard from "../cards/ProgramCard";
import Carousel from "../common/Carousel";

const ProgramFocus = ({ programs }) => {
  const [uniquePrograms, setUniquePrograms] = useState([]);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [groupedPrograms, setGroupedPrograms] = useState({});
  const [showProgramSelector, setShowProgramSelector] = useState(false);

  useEffect(() => {
    const categorizedPrograms = programs.reduce((acc, program) => {
      const category = program.category;
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push(program);
      return acc;
    }, {});

    setUniquePrograms(Object.keys(categorizedPrograms));
    setGroupedPrograms(categorizedPrograms);
  }, [programs]);

  const handleAddProgram = () => {
    setShowProgramSelector(true);
  };

  return (
    <Row>
      {uniquePrograms.map((program, index) => {
        return (
          <Col key={index} md={4}>
            <Card onClick={() => setSelectedProgram(program)}>
              <Card.Header>{program}</Card.Header>
              {/* ADD IMAGES */}
            </Card>
          </Col>
        );
      })}
      {selectedProgram && groupedPrograms[selectedProgram] ? (
        <Carousel>
          {groupedPrograms[selectedProgram].map((program, index) => {
            return <ProgramCard key={index} program={program} />;
          })}
        </Carousel>
      ) : null}

      <Col md={1}>
        <AddButton onClick={handleAddProgram} />
      </Col>
    </Row>
  );
};

ProgramFocus.propTypes = {
  programs: PropTypes.array.isRequired,
};

export default ProgramFocus;
