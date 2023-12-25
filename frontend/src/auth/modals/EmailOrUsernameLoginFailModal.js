import { useEffect } from "react";
import Modal from "react-bootstrap/Modal";

export const EmailOrUsernameLoginFail = ({ show, setShow }) => {
  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  useEffect(() => {
    const timeout = setTimeout(() => {
      handleClose();
    }, 3000);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title className="blue-text">Login Fail</Modal.Title>
        </Modal.Header>
        <Modal.Body className="blue-text">
          The username or password provided is incorrect. Please try again.
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
