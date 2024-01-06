import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";

const TheShed = () => {
  const user = useUser();
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
