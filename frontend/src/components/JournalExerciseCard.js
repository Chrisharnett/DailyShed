import React, { useState } from "react";
import {
  Card,
  Modal,
  Button,
  Container,
  Row,
  Col,
  Table,
} from "react-bootstrap";

const JournalExerciseCard = ({ exercise }) => {
  const [showModal, setShowModal] = useState(false);

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  return (
    <>
      <Card onClick={handleShow} style={{ cursor: "pointer" }}>
        <Card.Img
          className="journalImage"
          variant="top"
          src={exercise.imageFilename}
        />
      </Card>

      <Modal
        show={showModal}
        onHide={handleClose}
        aria-labelledby="Exercise History Details"
        className="glassModal"
      >
        <Modal.Header closeButton>
          <Modal.Title id="exerciseHistoryDetails">
            {exercise.exerciseName}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body className="journalModalBody">
          <Row>
            <Col>
              <p>Total Plays: {exercise.playCount}</p>
            </Col>
            <Col>
              <p>Average Rating: {exercise.averageRating}</p>
            </Col>
          </Row>
          <h5>Play History</h5>
          <Container className="historyContainer">
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Rating</th>
                  <th>Comment</th>
                </tr>
              </thead>
              <tbody>
                {exercise.playHistory.map((play, i) => {
                  return (
                    <tr className="journalEntry" key={i}>
                      <td>{play.date}</td>
                      <td>{play.rating}</td>
                      <td>{play.comment}</td>
                    </tr>
                  );
                })}
              </tbody>
            </Table>
          </Container>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default JournalExerciseCard;
