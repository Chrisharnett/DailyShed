import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Form, Button, Container, Modal } from "react-bootstrap";
import axios from "axios";

export const SelfAssessmentModal = ({ show, setShow, exercise, userData }) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [rating, setRating] = useState("");
  const [comment, setComment] = useState("");

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const navigate = useNavigate();

  const handleSelfAssessment = () => {
    const updateUser = async () => {
      try {
        const exerciseEntry = {
          exercise: exercise,
          rating: rating,
          comment: comment,
          timestamp: new Date().toISOString(),
        };
        userData.exerciseHistory.push(exerciseEntry);
        const response = await axios.post("/api/updateUserData", userData);
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
            <Modal.Title className=""> How did you perform? </Modal.Title>
          </Modal.Header>
          <Modal.Body className="">
            <Form className="container w-50 justify-content-center">
              {errorMessage && <div className="fail">{errorMessage}</div>}
              <Form.Group className="mb-3">
                <Form.Label className="" htmlFor="rating">
                  Rating (1-5):
                </Form.Label>
                {[1, 2, 3, 4, 5].map((value) => (
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
              <Form.Group className="mb-3">
                <Form.Label className="" htmlFor="rating">
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
