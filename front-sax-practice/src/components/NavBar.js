import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";

const Navigation = () => {
  return (
    <Navbar expand="lg" className="navbar-dark bg-dark p-2">
      <Container>
        <Navbar.Brand href="/">The Daily Shed</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/teacher">Teacher</Nav.Link>
            <Nav.Link href="/studentExercisePage/Paula">
              Student Exercise Page
            </Nav.Link>
            <Nav.Link href="/exerciseList">Exercise List</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
