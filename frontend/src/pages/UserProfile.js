import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import useUser from "../auth/useUser";
import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import axios from "axios";
import Card from "react-bootstrap/Card";

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const user = useUser();
  // const { handleSubmit } = useForm();

  useEffect(() => {
    const getUserData = async () => {
      try {
        const response = await axios.get(`/api/getUserData/${user.sub}`);
        if (response.data.userData) {
          setUserData(response.data.userData);
        } else {
          setUserData(null);
        }
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getUserData();
  }, [user]);

  const handleSubmit = async (data) => {};

  return (
    <>
      <Container>
        <h1>User Profile</h1>
        <p>Profile Info Form to update user data</p>
        <p>Your practice Session</p>
        <Card>
          <Card.Body>
            <Card.Title>name</Card.Title>
            <Card.Title>Current Practice Session</Card.Title>
            <Form
              onSubmit={handleSubmit()}
              className="container w-50 justify-content-center"
            >
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Current Goal</Form.Label>
                <Form.Control />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Key</Form.Label>
                <Form.Control />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Tone Collection</Form.Label>
                <Form.Control />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Key</Form.Label>
                <Form.Control />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Rounds</Form.Label>
                <Form.Control />
              </Form.Group>

              {/* TODO: Add the ability to change the number of Exercises */}
              {/* TODO: Allow Custom Exercises */}
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Exercise Selection</Form.Label>
                <Form.Control />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Tone Collection</Form.Label>
                <Form.Control />
              </Form.Group>
            </Form>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default UserProfile;
