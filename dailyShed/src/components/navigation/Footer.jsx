import { Nav, Navbar, Container } from "react-bootstrap";
import { InFromBelowAnimation } from "../../animation/animations";

const Footer = () => {
  return (
    <Navbar className="navbar-dark bg-black p-2 fixed-bottom mt-2">
      <Container
        fluid
        className="d-flex justify-content-between align-items-center"
      >
        <InFromBelowAnimation>
          <Navbar.Text className="">HarnettMusic 2023</Navbar.Text>
        </InFromBelowAnimation>
        <Nav>
          <InFromBelowAnimation>
            <Nav.Link className="" href="#top">
              Back to Top
            </Nav.Link>
          </InFromBelowAnimation>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Footer;
