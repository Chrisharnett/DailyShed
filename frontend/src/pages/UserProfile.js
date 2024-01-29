import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import useUser from "../auth/useUser";
import { useForm } from "react-hook-form";
import Col from "react-bootstrap/Col";
import { useState, useEffect } from "react";
import axios from "axios";
import Card from "react-bootstrap/Card";
import CollectionForm from "../components/CollectionForm";
import ExerciseDetailsForm from "../components/ExerciseDetailsForm";

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

  const { name, exerciseHistory, email, previousSet, program } = userData || {};

  const handleSubmit = async (data) => {};

  if (!userData) {
    return <p>Loading...</p>;
  }
  return (
    <>
      <Container>
        <h1>User Profile</h1>
        <p>Profile Info Form to update user data</p>
        <Card>
          <Card.Body>
            <Card.Title>{name}</Card.Title>
            <Form
              onSubmit={handleSubmit()}
              className="container w-50 justify-content-center"
            >
              {program.collections.map((collection, i) => {
                return (
                  <Col key={i}>
                    <CollectionForm key={i} collection={collection} />
                  </Col>
                );
              })}

              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Rounds</Form.Label>
                <Form.Control />
              </Form.Group>

              {/* TODO: Add the ability to change the number of Exercises */}
              {/* TODO: Allow Custom Exercises */}
              {program.exerciseDetails.map((details, i) => {
                return (
                  <Col key={i}>
                    <ExerciseDetailsForm key={i} details={details} />
                  </Col>
                );
              })}
            </Form>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default UserProfile;
