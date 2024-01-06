import Container from "react-bootstrap/Container";

const UserProfile = ({ user }) => {
  const { name } = user;
  return (
    <>
      <Container>
        <h1>User Profile</h1>
        <h2>{name}</h2>
      </Container>
    </>
  );
};

export default UserProfile;
