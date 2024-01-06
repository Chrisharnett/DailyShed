import Container from "react-bootstrap/Container";

const TheShed = ({ user }) => {
  const { name } = user;
  return (
    <>
      <Container>
        <h1>The Shed</h1>
        <h2>{name}</h2>
        <p>Under Construction</p>
      </Container>
    </>
  );
};

export default TheShed;
