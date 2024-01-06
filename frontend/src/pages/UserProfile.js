import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";

const UserProfile = () => {
  const user = useUser();
  const { name } = user;
  return (
    <>
      <Container>
        <h1>User Profile</h1>
        <h2>{name}</h2>
        <p>Under Construction</p>
      </Container>
    </>
  );
};

export default UserProfile;
