import PropTypes from "prop-types";
import AnimatedButton from "../common/AnimatedButton";

const RoutineSummary = ({ onNext }) => {
  const handleRoutineSummarySelect = (summary) => {
    onNext(summary);
  };

  return (
    <div>
      <h2>Routine Summary</h2>
      <AnimatedButton
        handleOnClick={() => handleRoutineSummarySelect("Accept")}
        buttonText={"Accept"}
      />
    </div>
  );
};

RoutineSummary.propTypes = {
  onNext: PropTypes.func.isRequired,
};

export default RoutineSummary;
