const AddButton = ({ onClick }) => {
  return (
    <div className="addIntervalButtonContainer">
      <button type="button" className="addIntervalButton" onClick={onClick}>
        +
      </button>
    </div>
  );
};

export default AddButton;
