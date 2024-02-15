import { Container, Form, Row, Col, Card, Button } from "react-bootstrap";
import useUser from "../auth/useUser";
import { useState, useEffect } from "react";
import axios from "axios";
import CollectionCard from "../components/CollectionCard";
import ExerciseDetailsForm from "../components/ExerciseDetailsForm";
import SuccessModal from "../components/SuccessModal";
import TopSpacer from "../util/TopSpacer";

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
      // newUserData.program = userData.program;
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
    const prevUserData = { ...userData };
    const newExerciseDetails = [...prevUserData.program.exerciseDetails];
    newExerciseDetails[index] = updatedDetails;
    setUserData((prevUserData) => ({
      ...prevUserData,
      program: {
        ...prevUserData.program,
        exerciseDetails: newExerciseDetails,
      },
    }));
  };

  if (!userData) {
    return (
      <>
        <div style={{ height: "5vh" }}></div>
        <p>Loading...</p>;
      </>
    );
  }
  return (
    <>
      <TopSpacer></TopSpacer>
      <Container className="midLayer glass">
        <h1 className="dropShadow"> {name} </h1>
        <Form
          onSubmit={handleSubmit}
          className="container justify-content-center"
        >
          <Container>
            <h2 className="dropShadow">Your practice routine</h2>
            <hr></hr>
            <h4 className="dropShadow">Your Collections</h4>
            <Row>
              {userData.program.collections.map((collection, i) => {
                return (
                  <Col key={i} className="mb-2" xs={12} sm={4}>
                    <CollectionCard i={i} collection={collection} />
                  </Col>
                );
              })}
            </Row>
            <hr></hr>
            {/* TODO: Add the ability to change the number of Exercises */}
            {/* TODO: Allow Custom Exercises */}
            <Form.Group as={Row} className="align-items-center dropShadow fs-3">
              <Form.Label className="dropShadow">Exercises</Form.Label>
              <Row>
                {userData.program.exerciseDetails.map((details, i) => {
                  return (
                    <Col key={i} xs={12} sm={3}>
                      <ExerciseDetailsForm
                        i={i}
                        details={details}
                        collections={userData.program.collections}
                        onDetailsChange={(updatedDetails) =>
                          handleDetailsChange(i, updatedDetails)
                        }
                      />
                    </Col>
                  );
                })}
              </Row>
            </Form.Group>

            <hr></hr>
            <Form.Group
              as={Row}
              className="align-items-center dropShadow fs-3"
              controlId="roundsSelector"
            >
              <Form.Label style={{ width: "auto" }} className="dropShadow">
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
            <Button variant="primary" type="submit" className="mt-2">
              Save Routine
            </Button>
          </Container>
        </Form>
      </Container>
      <SuccessModal
        show={openSuccessMessage}
        setShow={setOpenSuccessMessage}
        message={message}
      />
      <TopSpacer></TopSpacer>
    </>
  );
};

export default UserProfile;
