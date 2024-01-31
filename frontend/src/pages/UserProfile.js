import { Container, Form, Row, Col, Card, Button } from "react-bootstrap";
import useUser from "../auth/useUser";
import { useState, useEffect } from "react";
import axios from "axios";
import CollectionCard from "../components/CollectionCard";
import ExerciseDetailsForm from "../components/ExerciseDetailsForm";
import SuccessModal from "../components/SuccessModal";

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");

  const user = useUser();

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

  const { name } = userData || {};

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      let newUserData = { ...userData };
      newUserData.program = userData.program;
      setUserData(newUserData);
      await axios.post("/api/updateUserData", newUserData);
      setMessage("Routine Saved!");
      setOpenSuccessMessage(true);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const handleRoundsChange = (event) => {
    const newRounds = parseInt(event.target.value);
    setUserData((prevUserData) => ({
      ...prevUserData,
      program: {
        ...prevUserData.program,
        rounds: newRounds,
      },
    }));
  };

  const handleDetailsChange = (index, updatedDetails) => {
    setUserData((prevUserData) => {
      const newExerciseDetails = [...prevUserData.program.exerciseDetails];
      newExerciseDetails[index] = updatedDetails;
      return {
        ...prevUserData,
        program: {
          ...prevUserData.program,
          exerciseDetails: newExerciseDetails,
        },
      };
    });
  };

  if (!userData) {
    return <p>Loading...</p>;
  }
  return (
    <>
      <Container className="midLayer glass">
        <h1>{name}</h1>

        <div className="glass">
          <Form
            onSubmit={handleSubmit}
            className="container justify-content-center"
          >
            <Card
              style={{
                backdropFilter: "blur(10px) saturate(99%)",
                WebkitBackdropFilter: "blur(21px) saturate(99%)",
                backgroundColor: "rgba(228, 227, 227, 0.15)",
                border: "1px solid rgba(255, 255, 255, 0.125)",
                borderRadius: "15px",
                // color:
              }}
            >
              <Card.Body>
                <Card.Title>Your practice routine</Card.Title>

                <p>Active Collections:</p>
                {userData.program.collections.map((collection, i) => {
                  return (
                    <Col key={i} className="mb-2">
                      <CollectionCard i={i} collection={collection} />
                    </Col>
                  );
                })}
                <hr></hr>
                <Form.Group
                  as={Row}
                  className="mb-IT's be3"
                  controlId="roundsSelector"
                >
                  <Form.Label column sm="1">
                    Rounds:
                  </Form.Label>
                  <Col sm="1">
                    <Form.Control
                      type="number"
                      value={userData.program.rounds}
                      onChange={handleRoundsChange}
                      min="1"
                    />
                  </Col>
                </Form.Group>
                <hr></hr>

                {/* TODO: Add the ability to change the number of Exercises */}
                {/* TODO: Allow Custom Exercises */}
                {userData.program.exerciseDetails.map((details, i) => {
                  return (
                    <Col key={i}>
                      <ExerciseDetailsForm
                        i={i}
                        index={i}
                        details={details}
                        collections={userData.program.collections}
                        onDetailsChange={(updatedDetails) =>
                          handleDetailsChange(i, updatedDetails)
                        }
                      />
                    </Col>
                  );
                })}
              </Card.Body>
              <Card.Footer>
                <Button variant="primary" type="submit">
                  Save Routine
                </Button>
              </Card.Footer>
            </Card>
          </Form>
        </div>
      </Container>
      <SuccessModal
        show={openSuccessMessage}
        setShow={setOpenSuccessMessage}
        message={message}
      />
      <br></br>
      <br></br>
      <br></br>
    </>
  );
};

export default UserProfile;
