import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { Nav } from "react-bootstrap";

const Footer = () => {
  return (
    <Navbar className="navbar-dark bg-dark p-2 fixed-bottom">
      <Container>
        <Navbar.Brand className="">
          <h6>Copyright 2023</h6>
        </Navbar.Brand>
        <Nav>
          <Nav.Link className="" href="#top">
            <h6>Back to Top</h6>
          </Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Footer;
