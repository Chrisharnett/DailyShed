import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Form, Button, Container, Modal } from "react-bootstrap";
import axios from "axios";
import updatePlayerMetadata from "../util/UpdatePlayerMetadata.js";

export const SelfAssessmentModal = ({
  show,
  setShow,
  sessionID,
  exercise,
  currentSet,
  user,
  exerciseCount,
  setShowSessionCompleteModal,
  goToNextExercise,
  rounds,
}) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [rating, setRating] = useState("");
  const [comment, setComment] = useState("");

  const ratings = [1, 2, 3, 4, 5];

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const handleSelfAssessment = async () => {
    try {
      const exerciseEntry = {
        sessionID: sessionID,
        timestamp: new Date().toISOString(),
        sub: user.sub,
        exerciseID: exercise.exerciseID,
        rating: rating,
        comment: comment,
      };

      const logEntry = await axios.post("/api/logExercise", exerciseEntry);

      if (exerciseCount === currentSet.length * rounds) {
        setShowSessionCompleteModal(true);
      } else {
        goToNextExercise();
      }

      handleClose();
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const handleRatingChange = (e) => {
    setRating(e.target.value);
  };

  return (
    <>
      <Container className="container">
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title className=""> Journal Entry </Modal.Title>
          </Modal.Header>
          <Modal.Body className="">
            <Form className="container w-50 justify-content-center">
              {errorMessage && <div className="fail">{errorMessage}</div>}

              <Row>
                <Form.Group className="mb-3">
                  <Form.Label className="" htmlFor={`rating-1`}>
                    Rating (1-5):
                  </Form.Label>
                  {ratings.map((value) => (
                    <Form.Check
                      key={value}
                      inline
                      label={value}
                      name="rating"
                      type="radio"
                      id={`rating-${value}`}
                      value={value}
                      onChange={handleRatingChange}
                      checked={rating === value.toString()}
                    />
                  ))}
                </Form.Group>
              </Row>

              <Form.Group className="mb-3">
                <Form.Label className="" htmlFor="comments">
                  Comments{" "}
                </Form.Label>
                <Form.Control
                  id="comments"
                  placeholder="Were your dynamics great? Was your sound heavenly?"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Row className="container justify-content-center">
              <Button
                disabled={!rating}
                className="mx-3"
                onClick={handleSelfAssessment}
              >
                Submit
              </Button>
            </Row>
          </Modal.Footer>
        </Modal>
      </Container>
    </>
  );
};
