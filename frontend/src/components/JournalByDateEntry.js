import { Container } from "react-bootstrap";

const JournalByDateEntry = ({ journalEntry }) => {
  if (journalEntry) {
    return (
      <>
        <Container className="cardContainer d-flex flex-column align-items-center">
          JOURNAL ENTRY
        </Container>
      </>
    );
  }
};

export default JournalByDateEntry;
