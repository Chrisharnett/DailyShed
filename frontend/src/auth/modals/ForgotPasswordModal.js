import { useState } from "react";
import { Form, Modal, Button, Row } from "react-bootstrap";
import axios from "axios";
import { PasswordResetLandingModal } from "./PasswordResetLandingModal";

export const ForgotPasswordModal = ({ show, setShow }) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [emailValue, setEmailValue] = useState("");
  const [showPasswordResetLandingModal, setShowPasswordResetLandingModal] =
    useState(false);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const handleSubmitClicked = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`/api/forgotPassword/${emailValue}`);
      setShowPasswordResetLandingModal(true);
      handleClose();
    } catch (e) {
      setErrorMessage(e.response.data.message);
    }
  };

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text">Forgot Password</Modal.Title>
        </Modal.Header>
        <Form
          onSubmit={handleSubmitClicked}
          className="container w-50 justify-content-center"
        >
          <Modal.Body className="blue-text">
            Enter your email and we'll send a reset link.
            {errorMessage && <div className="fail">{errorMessage}</div>}
            <Form.Group className="mb-3">
              <Form.Label className="blue-text my-3" htmlFor="emailValue">
                Email:{" "}
              </Form.Label>
              <Form.Control
                value={emailValue}
                onChange={(e) => setEmailValue(e.target.value)}
                placeholder="email@email.com"
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>

            <Row className="container justify-content-center">
              <Button
                type="submit"
                className="green-button mx-3"
                disabled={!emailValue}
              >
                Submit
              </Button>
            </Row>
            
          </Modal.Footer>
        </Form>
      </Modal>
      <PasswordResetLandingModal
        show={showPasswordResetLandingModal}
        setShow={setShowPasswordResetLandingModal}
        emailValue={emailValue}
      />
    </>
  );
};
