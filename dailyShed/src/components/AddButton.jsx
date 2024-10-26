import PropTypes from "prop-types";

const AddButton = ({ onClick }) => {
  return (
    <div className="addIntervalButtonContainer">
      <button type="button" className="addIntervalButton" onClick={onClick}>
        +
      </button>
    </div>
  );
};

AddButton.propTypes = {
  onClick: PropTypes.func,
};

export default AddButton;
