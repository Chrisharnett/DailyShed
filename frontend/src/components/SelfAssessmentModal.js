import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Form, Button, Container, Modal } from "react-bootstrap";
import axios from "axios";

export const SelfAssessmentModal = ({ show, setShow }) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [selfAssessment, setSelfAssessment] = useState(null);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const navigate = useNavigate();

  //Write this.
  const handleSelfAssessment = () => {};

  return (
    <>
      <Container className="container">
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title className="blue-text"> Sign Up </Modal.Title>
          </Modal.Header>
          <Modal.Body className="blue-text">
            <Form className="container w-50 justify-content-center">
              {errorMessage && <div className="fail">{errorMessage}</div>}
              <Form.Group className="mb-3">
                <Form.Label className="blue-text" htmlFor="email">
                  Your Email Address:{" "}
                </Form.Label>
                <Form.Control
                  id="email"
                  placeholder="email@example.com"
                  value={selfAssessment}
                  onChange={(e) => setSelfAssessment(e.target.value)}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Row className="container justify-content-center">
              <Button
                disabled={!selfAssessment}
                className="mx-3"
                onClick={handleSelfAssessment()}
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
