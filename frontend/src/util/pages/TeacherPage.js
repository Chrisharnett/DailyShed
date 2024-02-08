import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";

const TeacherPage = () => {
  const user = useUser();
  return (
    <>
      <Container>
        <h1> This is the teacher page!</h1>
        <p>Under Construction</p>
      </Container>
    </>
  );
};

export default TeacherPage;
