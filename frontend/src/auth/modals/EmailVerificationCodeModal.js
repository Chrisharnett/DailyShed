import { useState } from "react";
import axios from "axios";
import { EmailVerificationSuccess } from "./EmailVerificationSuccess";
import { EmailVerificationFail } from "./EmailVerificationFail";
import { useToken } from "../../auth/useToken";
import Button from "react-bootstrap/Button";
import { Form } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";

export const EmailVerificationCodeModal = ({ show, setShow, email }) => {
  const [verificationString, setVerificationString] = useState("");
  const [showEmailVerificationSuccess, setShowEmailVerificationSuccess] =
    useState(false);
  const [showEmailVerificationFail, setShowEmailVerificationFail] =
    useState(false);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const [, setToken] = useToken();

  const onSubmitVerificationString = async () => {
    try {
      const response = await axios.put("/api/verifyEmail", {
        email,
        verificationString,
      });
      const { token } = response.data;
      setToken(token);
      setShowEmailVerificationSuccess(true);
      handleClose();
    } catch (e) {
      setShowEmailVerificationFail(true);
      handleClose();
    }
  };

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text">
            Please Verify Your Email
          </Modal.Title>
        </Modal.Header>
        <Form className="container w-50 justify-content-center">
          <Modal.Body className="blue-text">
            <p className="blue-secondary-header">
              You should have received a verification code at the email you
              provided.
            </p>
            <Form.Group>
              <Form.Label className="blue-text" htmlFor="verification">
                Verification Code:{" "}
              </Form.Label>
              <Form.Control
                value={verificationString}
                id="verification"
                onChange={(e) => setVerificationString(e.target.value)}
                placeholder="123456"
              />
            </Form.Group>
            <hr></hr>
            <Button
              onClick={onSubmitVerificationString}
              className="green-button mx-3"
            >
              Submit
            </Button>
          </Modal.Body>
        </Form>
        <Modal.Footer></Modal.Footer>
      </Modal>
      <EmailVerificationSuccess
        show={showEmailVerificationSuccess}
        setShow={setShowEmailVerificationSuccess}
      />
      <EmailVerificationFail
        show={showEmailVerificationFail}
        setShow={setShowEmailVerificationFail}
      />
    </>
  );
};
