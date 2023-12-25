import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Form, Button, Container, Modal } from "react-bootstrap";
import axios from "axios";
import { useToken } from "../../auth/useToken.js";
import { PasswordRequirements } from "../../auth/PasswordRequirements.js";
import {
  RealTimeValidation,
  initialConditionsMet,
} from "../../auth/RealTimeValidation.js";
import { UsernameExistsSignUpFailModal } from "./UsernameExistsSignUpFailModal.js";
import { EmailVerificationCodeModal } from "./EmailVerificationCodeModal.js";

export const SignUpModal = ({
  show,
  setShow,
  showLoginModal,
  setShowLoginModal,
}) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useToken();
  const [emailValue, setEmailValue] = useState("");
  const [passwordValue, setPasswordValue] = useState("");
  const [confirmPasswordValue, setConfirmPasswordValue] = useState("");
  const [conditionsMet, setConditionsMet] = useState(initialConditionsMet);
  const [showUserNameExistsSignUpFail, setShowUserNameExistsSignUpFail] =
    useState(false);
  const [showEmailVerificationModal, setShowEmailVerificationModal] =
    useState(false);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const navigate = useNavigate();

  const onSignUpClicked = async () => {
    const max_properties = 3;
    try {
      const response = await axios.post("/api/signup", {
        email: emailValue,
        password: passwordValue,
        max_properties: max_properties,
      });

      const { token } = response.data;
      setToken(token);
      setShowEmailVerificationModal(true);
      handleClose();
    } catch (error) {
      if (error.response.data.error === "UsernameExistsException") {
        setShowUserNameExistsSignUpFail(true);
        handleClose();
      } else {
        console.error("Login error:", error);
      }
    }
  };

  const handlePasswordChange = (value, conditions) => {
    setPasswordValue(value);
    setConditionsMet(conditions);
  };

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
                  value={emailValue}
                  onChange={(e) => setEmailValue(e.target.value)}
                />
              </Form.Group>

              <RealTimeValidation
                passwordValue={passwordValue}
                onPasswordChange={handlePasswordChange}
              />

              <Form.Group className="mb-3">
                <Form.Label className="blue-text" htmlFor="confirm">
                  Confirm Password:{" "}
                </Form.Label>
                <Form.Control
                  id="confirm"
                  type="password"
                  placeholder="password"
                  value={confirmPasswordValue}
                  onChange={(e) => setConfirmPasswordValue(e.target.value)}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <hr></hr>
            <PasswordRequirements conditionsMet={conditionsMet} />
            <hr></hr>

            <Row className="container justify-content-center">
              <Button
                disabled={
                  !emailValue ||
                  !passwordValue ||
                  passwordValue !== confirmPasswordValue
                }
                className="green-button mx-3"
                onClick={onSignUpClicked}
              >
                Sign Up
              </Button>
            </Row>
            
            <Row className="container justify-content-center">
              <Button
                className="green-button mx-3"
                onClick={() => {
                  setShowLoginModal(true);
                  handleClose();
                }}
              >
                Have an account? Log in!
              </Button>
            </Row>

          </Modal.Footer>
        </Modal>
      </Container>
      <UsernameExistsSignUpFailModal
        show={showUserNameExistsSignUpFail}
        setShow={setShowUserNameExistsSignUpFail}
        setShowLoginModal={setShowLoginModal}
      />
      <EmailVerificationCodeModal
        show={showEmailVerificationModal}
        setShow={setShowEmailVerificationModal}
        email={emailValue}
      />
    </>
  );
};
