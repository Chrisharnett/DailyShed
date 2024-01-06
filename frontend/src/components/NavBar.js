import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { useToken } from "../auth/useToken";
import useUser from "../auth/useUser.js";
import axios from "axios";

const Navigation = ({ user, loggedIn, setLoggedIn }) => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [, setToken] = useToken();
  const [, setUser] = useState(null);
  const [cognitoURL, setCognitoURL] = useState("");
  const navigate = useNavigate();

  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  useEffect(() => {
    if (token) {
      setToken(token);
      setLoggedIn(true);
    }
  }, [token, setToken, navigate, setLoggedIn]);

  useEffect(() => {
    const loadCognitoURL = async () => {
      try {
        const response = await axios.get("/api/auth/cognito/url");
        const { url } = response.data;
        setCognitoURL(url);
      } catch (e) {
        console.log(e);
      }
    };
    loadCognitoURL();
  }, []);

  useEffect(() => {
    if (user) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, [user, setLoggedIn]);

  const logOutHandler = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
    navigate("/");
  };

  return (
    <>
      <Navbar expand="lg" className="navbar-dark bg-dark p-2" id="top">
        <Container>
          <Navbar.Brand href="/">The Daily Shed</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            {loggedIn && (
              <Nav className="me-auto">
                <Nav.Link href="/theShed">The Shed</Nav.Link>
                <Nav.Link href="/userProfile">User Profile</Nav.Link>
                <Nav.Link href="/practiceJournal">Practice Journal</Nav.Link>
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
