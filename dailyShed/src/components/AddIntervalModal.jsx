import { Modal, Button, Form } from "react-bootstrap";
import { useState } from "react";
import PropTypes from "prop-types";

const AddIntervalModal = ({
  show,
  setShow,
  programs,
  addIntervalToSession,
}) => {
  const handleClose = () => setShow(false);
  const [reviewBool, setReviewExercise] = useState(false);
  const [selectedProgramID, setSelectedProgramID] = useState(
    programs[0]?.programID || null
  );

  const handleCheckboxChange = (e) => {
    e.preventDefault();
    setReviewExercise(e.target.checked);
  };

  const handleProgramChange = (e) => {
    setSelectedProgramID(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newProgram = programs.find(
      (program) => program.programID === parseInt(selectedProgramID)
    );
    const newInterval = {
      currentIndex: newProgram.currentIndex,
      primaryCollectinID: newProgram.primaryCollection.primaryCollectionID,
      programID: newProgram.programID,
      rhythmCollectionID: newProgram.rhythmCollection.rhythmCollectionID,
      sacleTonicIndex: newProgram.tonic.scaleTonicIndex,
      reviewExercise: reviewBool,
    };
    addIntervalToSession(newInterval);
    handleClose();
  };

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text">Add an exercise.</Modal.Title>
        </Modal.Header>
        <Form
          onSubmit={handleSubmit}
          className="container justify-content-center"
        >
          <Modal.Body className="blue-text"></Modal.Body>
          <Form.Label className="blue-text">Your Programs</Form.Label>
          <Form.Select value={selectedProgramID} onChange={handleProgramChange}>
            {programs.map((program, index) => (
              <option key={index} value={program.programID}>
                {program.primaryCollection.primaryCollectionTitle}
              </option>
            ))}
          </Form.Select>
          <hr></hr>
          <Form.Check
            type="checkbox"
            label="Review Exercise"
            checked={reviewBool}
            onChange={handleCheckboxChange}
            className="dropShado"
          />
          <Modal.Footer>
            <Button variant="primary" type="submit">
              Add Exercise
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
};

AddIntervalModal.propTypes = {
  show: PropTypes.bool,
  setShow: PropTypes.func,
  programs: PropTypes.array,
  addIntervalToSession: PropTypes.func,
};

export default AddIntervalModal;
