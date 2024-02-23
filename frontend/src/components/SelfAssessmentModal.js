import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Form, Button, Container, Modal } from "react-bootstrap";
import axios from "axios";

export const SelfAssessmentModal = ({
  show,
  setShow,
  exercise,
  currentSet,
  player,
  setPlayer,
}) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [rating, setRating] = useState("");
  const [comment, setComment] = useState("");

  const ratings = [1, 2, 3, 4, 5];

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const handleSelfAssessment = () => {
    const updateUser = async () => {
      try {
        const timestamp = new Date().toISOString();
        const exerciseEntry = {
          timestamp: timestamp,
          sub: player.sub,
          exercise: {
            name: exercise.fileName,
            notePatternRhythmLength:
              exercise.notePattern.notePatternRhythmLength,
            rhythmMatcher: exercise.rhythmPattern.rhythmDescription,
          },
          rating: rating,
          comment: comment,
        };
        const logEntry = await axios.post("/api/logExercise", exerciseEntry);
        // let newUserData = { ...player };
        // newUserData.exerciseHistory.push(exerciseEntry);
        // newUserData.previousSet = currentSet;
        // setPlayer(newUserData);
        // const response = await axios.post("/api/updateUserData", newUserData);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    updateUser();
    handleClose();
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
