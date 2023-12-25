import { useNavigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import { useEffect } from "react";

export const EmailVerificationSuccess = ({ show, setShow }) => {
  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);
  const navigate = useNavigate();

  useEffect(() => {
    const timeout = setTimeout(() => {
      // navigate(`/`);
      handleClose();
    }, 3000);
    return () => clearTimeout(timeout);
  }, [show]);

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text">Success!</Modal.Title>
        </Modal.Header>
        <Modal.Body className="blue-text">
          Welcome to Maintain. Log in to maintain your properties.
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
