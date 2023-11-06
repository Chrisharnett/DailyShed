import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import { useToken } from "../auth/useToken";
import axios from "axios";

const LoginPage = () => {
  const [emailValue, setEmailValue] = useState("");
  const [token, setToken] = useToken();
  const [passwordValue, setPasswordValue] = useState("");
  const [errorMessage, setError] = useState("");

  const navigate = useNavigate();

  const onLoginClicked = async () => {
    const response = await axios.post("/api/login", {
      email: emailValue,
      password: passwordValue,
    });

    const { token } = response.data;
    setToken(token);
    navigate("/exerciseTestPage");
  };

  return (
    <>
      <Container
        className="w-75 text-center main"
        style={{ backgroundColor: "#DAE2DF", height: 800 }}
      >
        <h1> Log-in. </h1>
        {errorMessage && <p className="fail">{errorMessage}</p>}
        <Form.Group className="mb-3">
          <Form.Label>Your Email Address</Form.Label>
          <Form.Control
            placeholder="Your email address"
            value={emailValue}
            onChange={(e) => setEmailValue(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Your password"
            value={passwordValue}
            onChange={(e) => setPasswordValue(e.target.value)}
          />
        </Form.Group>

        <Button
          disabled={!emailValue || !passwordValue}
          variant="success"
          onClick={onLoginClicked}
        >
          {" "}
          Log In{" "}
        </Button>

        <Button onClick={() => navigate("/forgotPassword")}>
          {" "}
          Forgot Password?{" "}
        </Button>

        <Button variant="custom" onClick={() => navigate("/createAccount")}>
          {" "}
          Don't have an account? Sign Up!{" "}
        </Button>
      </Container>
    </>
  );
};

export default LoginPage;
