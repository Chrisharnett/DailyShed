import { useEffect } from "react";
import Modal from "react-bootstrap/Modal";

export const PasswordResetSuccess = ({ show, setShow }) => {
  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  useEffect(() => {
    const timeout = setTimeout(() => {
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
          Your password has been reset. Please login with your new password.{" "}
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
