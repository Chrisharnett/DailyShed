import PropTypes from "prop-types";
import AnimatedButton from "../common/AnimatedButton";

const PracticeDebrief = ({ onNext }) => {
  const handleCompleteDebrief = () => {
    onNext(true);
  };

  return (
    <div>
      <h2>Practice Debrief</h2>
      <AnimatedButton
        handleOnClick={() => handleCompleteDebrief("Accept")}
        buttonText={"Accept"}
      />
    </div>
  );
};

PracticeDebrief.propTypes = {
  onNext: PropTypes.func.isRequired,
};

export default PracticeDebrief;
