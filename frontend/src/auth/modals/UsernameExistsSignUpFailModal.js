import { useEffect } from "react";
import Modal from "react-bootstrap/Modal";

export const UsernameExistsSignUpFailModal = ({ show, setShow }) => {
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
          <Modal.Title className="blue-text">Signup Fail</Modal.Title>
        </Modal.Header>
        <Modal.Body className="blue-text">
          That username already exists. Please try again. If you've forgotten
          your password, select 'Forgot Password' on the log in page.
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
