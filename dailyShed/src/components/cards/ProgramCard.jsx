import PropTypes from "prop-types";
import { Card } from "react-bootstrap";

const ProgramCard = ({ program }) => {
  return (
    <Card>
      <Card.Header>{program.PrimaryCollectionTitle}</Card.Header>
    </Card>
  );
};
ProgramCard.propTypes = {
  program: PropTypes.object.isRequired,
};

export default ProgramCard;
