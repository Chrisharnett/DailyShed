import { Card, Container } from "react-bootstrap";

const HomePage = () => {
  return (
    <>
      <Container className="midLayer glass">
        <Card
          style={{
            backdropFilter: "blur(10px) saturate(99%)",
            WebkitBackdropFilter: "blur(21px) saturate(99%)",
            backgroundColor: "rgba(228, 227, 227, 0.15)",
            border: "1px solid rgba(255, 255, 255, 0.125)",
            borderRadius: "15px",
            color: "rgb(255, 255, 255, 1)",
          }}
        >
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
