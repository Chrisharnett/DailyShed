import { useEffect } from "react";
import Modal from "react-bootstrap/Modal";

export const PasswordResetFail = ({ show, setShow }) => {
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
          <Modal.Title className="blue-text">Uh-Oh</Modal.Title>
        </Modal.Header>
        <Modal.Body className="blue-text">
          Something went wrong. Please try again.{" "}
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
