import { Nav, Navbar, Container } from "react-bootstrap";
import { InFromBelowAnimation } from "../animation/animations";

const Footer = () => {
  return (
    <Navbar className="navbar-dark bg-black p-2 fixed-bottom mt-2">
      <Container>
        <InFromBelowAnimation>
          <Navbar.Brand className="">
            <h6>Copyright 2023</h6>
          </Navbar.Brand>
        </InFromBelowAnimation>
        <Nav>
          <InFromBelowAnimation>
            <Nav.Link className="" href="#top">
              <h6>Back to Top</h6>
            </Nav.Link>
          </InFromBelowAnimation>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Footer;
