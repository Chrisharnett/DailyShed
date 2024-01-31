import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";

const SuccessModal = ({ show, setShow, message }) => {
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
          {message ? message : "Procedure completed!"}
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};

export default SuccessModal;
