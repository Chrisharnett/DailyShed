import { useState } from "react";
import axios from "axios";
import { PasswordResetSuccess } from "./PasswordResetSuccess";
import { PasswordResetFail } from "./PasswordResetFail";
import { Button } from "react-bootstrap";
import { Form } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";
import { PasswordRequirements } from "../PasswordRequirements.js";
import {
  RealTimeValidation,
  initialConditionsMet,
} from "../../auth/RealTimeValidation.js";

export const PasswordResetLandingModal = ({ show, setShow, emailValue }) => {
  const [passwordValue, setPasswordValue] = useState("");
  const [confirmPasswordValue, setConfirmPasswordValue] = useState("");
  const [passwordResetCode, setPasswordResetCode] = useState("");
  const [showPasswordResetSuccess, setShowPasswordResetSuccess] =
    useState(false);
  const [showPasswordResetFail, setShowPasswordResetFail] = useState(false);
  const [conditionsMet, setConditionsMet] = useState(initialConditionsMet);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const onResetClicked = async () => {
    try {
      await axios.put(`/api/users/${passwordResetCode}/reset-password`, {
        email: emailValue,
        newPassword: passwordValue,
      });
      setShowPasswordResetSuccess(true);
      handleClose();
    } catch (e) {
      setShowPasswordResetFail(true);
      handleClose();
    }
  };

  const handlePasswordChange = (value, conditions) => {
    setPasswordValue(value);
    setConditionsMet(conditions);
  };

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text"> Reset Password </Modal.Title>
        </Modal.Header>
        <Modal.Body className="blue-text">
          <p className="blue-secondary-header">Please enter a new password</p>
          <Form className="container w-50 justify-content-center">
            <Form.Group>
              <Form.Label className="blue-text" htmlFor="code">
                Reset Code:{" "}
              </Form.Label>
              <Form.Control
                value={passwordResetCode}
                id="code"
                onChange={(e) => setPasswordResetCode(e.target.value)}
                placeholder="123456"
              />
            </Form.Group>

            <RealTimeValidation
              passwordValue={passwordValue}
              onPasswordChange={handlePasswordChange}
            />

            <Form.Group>
              <Form.Label className="blue-text" htmlFor="confirm">
                Confirm Password:{" "}
              </Form.Label>
              <Form.Control
                type="password"
                id="confirm"
                value={confirmPasswordValue}
                onChange={(e) => setConfirmPasswordValue(e.target.value)}
                placeholder="Password"
              />
            </Form.Group>
            <hr></hr>

            <Button
              className="green-button mx-3"
              disabled={
                !passwordValue ||
                !confirmPasswordValue ||
                passwordValue !== confirmPasswordValue
              }
              onClick={onResetClicked}
            >
              Reset Password
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <hr></hr>
          <PasswordRequirements conditionsMet={conditionsMet} />
          <hr></hr>
        </Modal.Footer>
      </Modal>
      <PasswordResetSuccess
        show={showPasswordResetSuccess}
        setShow={setShowPasswordResetSuccess}
      />
      <PasswordResetFail
        show={showPasswordResetFail}
        setShow={setShowPasswordResetFail}
      />
    </>
  );
};
