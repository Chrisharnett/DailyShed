import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { useNavigate } from "react-router-dom";

const Navigation = ({ loggedIn, setLoggedIn, cognitoURL }) => {
  const navigate = useNavigate();

  const logOutHandler = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
    navigate("/");
  };

  return (
    <>
      <Navbar
        expand="lg"
        className="navbar-dark bg-black p-2 mb-2"
        id="top"
        fixed="top"
      >
        <Container>
          <Navbar.Brand href="/">The Daily Shed</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            {loggedIn && (
              <Nav className="me-auto">
                <Nav.Link href="/theShed">The Shed</Nav.Link>
                <Nav.Link href="/userProfile">My Practice Session</Nav.Link>
                <Nav.Link href="/programs">My Practice Programs</Nav.Link>
                <Nav.Link href="/practiceJournal">My Practice Journal</Nav.Link>
              </Nav>
            )}
            {loggedIn && (
              <Nav>
                <Nav.Link className="" href="#" onClick={logOutHandler}>
                  <h4>Logout</h4>
                </Nav.Link>
              </Nav>
            )}
            {!loggedIn && (
              <Nav>
                <Nav.Link
                  className=""
                  href="#login"
                  onClick={() => {
                    window.location.href = cognitoURL;
                  }}
                >
                  <h4>Login</h4>
                </Nav.Link>
              </Nav>
            )}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default Navigation;
