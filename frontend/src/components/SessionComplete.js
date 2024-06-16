import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Modal } from "react-bootstrap";

export const SessionCompleteModal = ({
  show,
  setShow,
  currentSet,
  setCreated,
}) => {
  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const navigate = useNavigate();

  useEffect(() => {
    if (show) {
      const timeout = setTimeout(() => {
        setCreated.current = false;
        navigate("/");
        handleClose();
      }, 1500);
      return () => clearTimeout(timeout);
    }
  }, [show]);

  return (
    <>
      <Container className="container">
        <Modal show={show} onHide={handleClose} className="glassModal">
          <Modal.Header closeButton>
            <Modal.Title className=""> Congratulations</Modal.Title>
          </Modal.Header>
          <Modal.Body className="">You have a new tool in the shed.</Modal.Body>
          <Modal.Footer>See you next time.</Modal.Footer>
        </Modal>
      </Container>
    </>
  );
};
