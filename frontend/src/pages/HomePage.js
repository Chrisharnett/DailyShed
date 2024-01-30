import { Card, Container } from "react-bootstrap";

const HomePage = () => {
  return (
    <>
      <Container className="midLayer">
        <Card>
          <Card.Body>
            <Card.Text>
              <h1> Welcome to the Daily Shed </h1>
              <br></br>
              <h2> A woodshedding practice app for saxophone players </h2>
              <br></br>
              <h3> Sign in for todays session, or sign-up to get started </h3>
              <br></br>
            </Card.Text>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default HomePage;
