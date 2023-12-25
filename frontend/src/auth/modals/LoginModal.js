import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Form, Button, Row } from "react-bootstrap";
import axios from "axios";
import { useToken } from "../../auth/useToken";
import { FcGoogle } from "react-icons/fc";
import { EmailOrUsernameLoginFail } from "./EmailOrUsernameLoginFailModal";
import { SignUpModal } from "./SignUpModal";
import { ForgotPasswordModal } from "./ForgotPasswordModal";
import Modal from "react-bootstrap/Modal";

export const LoginModal = ({ loggedIn, setLoggedIn, show, setShow }) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useToken();
  const [emailValue, setEmailValue] = useState("");
  const [passwordValue, setPasswordValue] = useState("");
  const [googleOauthUrl, setGoogleOauthUrl] = useState("");
  const [loginFailModalShow, setLoginFailModalShow] = useState(false);
  const [signUpModalShow, setSignUpModalShow] = useState(false);
  const [forgotPasswordModalShow, setForgotPasswordModalShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleOpen = () => setShow(true);

  const urlParams = new URLSearchParams(window.location.search);
  const oauthToken = urlParams.get("token");
  const navigate = useNavigate();

  useEffect(() => {
    const loadOauthUrl = async () => {
      try {
        const response = await axios.get("/api/auth/google/url");
        const { url } = response.data;
        setGoogleOauthUrl(url);
      } catch (e) {
        console.log(e);
      }
    };
    loadOauthUrl();
  }, []);

  const onLoginClicked = async () => {
    try {
      const response = await axios.post("/api/login", {
        email: emailValue,
        password: passwordValue,
      });
      const { token } = response.data;
      setToken(token);
      setLoggedIn(true);
      navigate("/displayProperties");
      handleClose();
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setLoginFailModalShow(true);
      } else {
        console.error("Login error:", error);
      }
    }
  };

  const onSignUpClicked = () => {
    setSignUpModalShow(true);
    handleClose();
  };

  return (
    <>
      <Container className="container">
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title className="blue-text">Login</Modal.Title>
          </Modal.Header>
          <Modal.Body className="blue-text">
            <Form className="container w-50 justify-content-center">
              {errorMessage && <div className="fail">{errorMessage}</div>}
              <Form.Group className="mb-3">
                <Form.Label className="blue-text" htmlFor="email">
                  Your Email Address:{" "}
                </Form.Label>
                <Form.Control
                  id="email"
                  placeholder="email@example.com"
                  value={emailValue}
                  onChange={(e) => setEmailValue(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label className="blue-text" htmlFor="password">
                  Password:{" "}
                </Form.Label>
                <Form.Control
                  id="password"
                  type="password"
                  placeholder="password"
                  value={passwordValue}
                  onChange={(e) => setPasswordValue(e.target.value)}
                />
              </Form.Group>
            </Form>{" "}
          </Modal.Body>
          <Modal.Footer>
            <Row className="container justify-content-center">
              <Button
                disabled={!emailValue || !passwordValue}
                className="green-button mx-3"
                onClick={onLoginClicked}
              >
                Log In
              </Button>
            </Row>


            <Row className="container justify-content-center">
              <Button className="green-button mx-3" onClick={onSignUpClicked}>
                Sign Up
              </Button>
            </Row>

            
            <Row className="container justify-content-center">
              <Button
                className="green-button mx-3"
                onClick={() => {
                  setForgotPasswordModalShow(true);
                  handleClose();
                }}
              >
                Forgot Password?
              </Button>
            </Row>

            <Row className="container justify-content-center">
              <Button
                className="google-sign-in-button m-3"
                style={{width: "fit-content"}}
                variant="custom"
                disabled={!googleOauthUrl}
                onClick={() => {
                  window.location.href = googleOauthUrl;
                }}
              >
                <FcGoogle className="google-icon" />
                Log in with Google
              </Button>
            </Row>
            

          </Modal.Footer>
        </Modal>
      </Container>
      <EmailOrUsernameLoginFail
        show={loginFailModalShow}
        setShow={setLoginFailModalShow}
      />
      <SignUpModal
        show={signUpModalShow}
        setShow={setSignUpModalShow}
        showLoginModal={show}
        setShowLoginModal={setShow}
      />
      <ForgotPasswordModal
        show={forgotPasswordModalShow}
        setShow={setForgotPasswordModalShow}
      />
    </>
  );
};
