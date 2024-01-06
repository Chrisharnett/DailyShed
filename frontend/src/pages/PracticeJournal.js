import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";

const PracticeJournal = () => {
  const user = useUser();
  const { name } = user;
  return (
    <>
      <Container>
        <h1>Practice Journal</h1>
        <h2>{name}</h2>
        <p>Under Construction</p>
      </Container>
    </>
  );
};

export default PracticeJournal;
