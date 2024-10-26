import Container from "react-bootstrap/Container";
import PropTypes from "prop-types";

const TeacherPage = (user) => {
  return (
    <>
      <Container>
        <h1> This is the teacher page!</h1>
        <p>Under Construction</p>
      </Container>
    </>
  );
};

TeacherPage.propTypes = {
  user: PropTypes.object,
};

export default TeacherPage;
