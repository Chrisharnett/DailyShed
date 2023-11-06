import { useState } from "react";
import { Link, useNavigate, useHistory } from "react-router-dom";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setError] = useState("");

  const navigate = useNavigate();
  const logIn = async () => {
    try {
      await signInWithEmailAndPassword(getAuth(), email, password);
      navigate("/studentExercisePage/John");
    } catch (e) {
      setError(e.message);
    }
  };

  const onLoginClicked = async () => {
    var requestOptions = {
      method: "GET",
      redirect: "follow",
    };

    fetch("api/login", requestOptions)
      .then((response) => response.json)
      .then((result) => console.log(result))
      .catch((e) => console.log("error", e));
  };

  return (
    <>
      <h1> Log-in. </h1>
      {errorMessage && <p className="fail">{errorMessage}</p>}
      <Form.Group className="mb-3">
        <Form.Label>Your Email Address</Form.Label>
        <Form.Control
          placeholder="Your email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </Form.Group>
      <Button variant="success" onClick={logIn}>
        {" "}
        Log In{" "}
      </Button>
      {/* From video in class, incomplete (obviously) */}
      <Button disabled={!email || !password} onClick={onLoginClicked()} />
      <Link to="/createAccount">Don't have an account? Create one here.</Link>
    </>
  );
};

export default LoginPage;
