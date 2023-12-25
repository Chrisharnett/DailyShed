import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { useToken } from "../auth/useToken";
import { LoginModal } from "../auth/modals/LoginModal.js";

const Navigation = ({ user, loggedIn, setLoggedIn }) => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [, setToken] = useToken();
  const navigate = useNavigate();

  const urlParams = new URLSearchParams(window.location.search);
  const oauthToken = urlParams.get("token");

  useEffect(() => {
    if (oauthToken) {
      setToken(oauthToken);
      setLoggedIn(true);
    }
  }, [oauthToken, setToken, navigate, setLoggedIn]);

  useEffect(() => {
    if (user) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, [user, setLoggedIn]);

  const logOutHandler = () => {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
    setLoggedIn(false);
    navigate("/");
  };
  return (
    <>
      <Navbar expand="lg" className="navbar-dark bg-dark p-2">
        <Container>
          <Navbar.Brand href="/">The Daily Shed</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/studentExercisePage/Paula">Shed Time</Nav.Link>
              <Nav.Link href="/studentProfile/Paula">User Profile</Nav.Link>
              <Nav.Link href="/practiceJournal/Paula">
                Practice Journal
              </Nav.Link>
            </Nav>
            {loggedIn && (
              <Nav className="me-auto">
                <Nav.Link className="green-text" href="/displayProperties">
                  <h4>Properties</h4>
                </Nav.Link>
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
                  onClick={setShowLoginModal}
                >
                  <h4>Login</h4>
                </Nav.Link>
              </Nav>
            )}
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <LoginModal
        loggedIn={loggedIn}
        setLoggedIn={setLoggedIn}
        show={showLoginModal}
        setShow={setShowLoginModal}
      />
    </>
  );
};

export default Navigation;
