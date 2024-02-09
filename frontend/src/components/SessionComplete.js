import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Modal } from "react-bootstrap";
import axios from "axios";

export const SessionCompleteModal = ({
  show,
  setShow,
  currentSet,
  userData,
  setUserData,
}) => {
  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const navigate = useNavigate();

  useEffect(() => {
    const timeout = setTimeout(() => {
      navigate("/practiceJournal");
      handleClose();
    }, 3000);
    return () => clearTimeout(timeout);
  }, [show]);

  useEffect(() => {
    if (show) {
      const updateUser = async () => {
        try {
          let newUserData = { ...userData };
          newUserData.previousSet = currentSet;
          setUserData(newUserData);
          await axios.post("/api/updateUserData", newUserData);
        } catch (error) {
          console.error("Error: ", error);
        }
      };
      updateUser();
    }
  }, [show, currentSet, userData, setUserData]);

  return (
    <>
      <Container className="container">
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title className=""> Congratulations</Modal.Title>
          </Modal.Header>
          <Modal.Body className="">You earned these achievements</Modal.Body>
          <Modal.Footer>Saving practice data. See you next time.</Modal.Footer>
        </Modal>
      </Container>
    </>
  );
};
