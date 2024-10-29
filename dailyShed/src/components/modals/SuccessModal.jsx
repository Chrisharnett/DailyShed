import { useEffect } from "react";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";

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

SuccessModal.propTypes = {
  show: PropTypes.bool,
  setShow: PropTypes.func,
  message: PropTypes.string,
};

export default SuccessModal;
