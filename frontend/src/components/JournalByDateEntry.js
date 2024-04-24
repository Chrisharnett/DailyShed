import { Container, Col, Row } from "react-bootstrap";
import JournalExerciseCard from "./JournalExerciseCard";
import formatDate from "../util/FormatDate";

const JournalByDateEntry = ({ journalEntry }) => {
  const date = formatDate(journalEntry[0].timestamp);
  if (journalEntry) {
    return (
      <>
        <Container className="cardContainer d-flex flex-column align-items-center">
          <h1>{date}</h1>
          {journalEntry.map((exercise, i) => {
            return (
              <>
                <Row>
                  <Col key={i} className="mb-2" xs={12} sm={4}>
                    <JournalExerciseCard exercise={exercise} />
                  </Col>
                </Row>
              </>
            );
          })}
        </Container>
      </>
    );
  }
};

export default JournalByDateEntry;
