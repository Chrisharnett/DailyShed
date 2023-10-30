import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";

const CreateAccountPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const createAccount = async () => {
    try {
      if (password !== confirmPassword) {
        setError("Passwords do not match!");
        return;
      }
      await createUserWithEmailAndPassword(getAuth(), email, password);
      navigate("/StudentExercisePage/Chloe");
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <>
      <h1> Create Account. </h1>
      {error && <p className="error">{error}</p>}
      <Form>
        <input
          placeholder="Your email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Confirm your password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </Form>
      <Button variant="success" onClick={createAccount}>
        Create Account
      </Button>
      <Button
        variant="success"
        onClick={() => history.pushState("/forgot-password")}
      >
        Create Account
      </Button>
      <Link to="/login">Already have an account? Log in here.</Link>
    </>
  );
};

export default CreateAccountPage;
