import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useState } from "react";
import CollectionCard from "../components/CollectionCard";
import ExerciseDetailsForm from "../components/ExerciseDetailsForm";
import SuccessModal from "../components/SuccessModal";
import TopSpacer from "../util/TopSpacer";

const UserProfile = ({ user, playerDetails, updatePlayerDetails }) => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const newUserData = { ...playerDetails };
    try {
      await updatePlayerDetails(newUserData);
      setMessage("Routine Saved!");
      setOpenSuccessMessage(true);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const handleRoundsChange = (event) => {
    const newRounds = parseInt(event.target.value);
    updatePlayerDetails({
      ...playerDetails,
      program: {
        ...playerDetails.program,
        rounds: newRounds,
      },
    });
  };

  const handleDetailsChange = (index, updatedDetails) => {
    const newExerciseDetails = [...playerDetails.program.exerciseDetails];
    newExerciseDetails[index] = updatedDetails;
    updatePlayerDetails({
      ...playerDetails,
      program: {
        ...playerDetails.program,
        exerciseDetails: newExerciseDetails,
      },
    });
  };

  if (!playerDetails) {
    return (
      <>
        <div style={{ height: "5vh" }}></div>
        <p>Loading...</p>;
      </>
    );
  } else {
    return (
      <>
        <TopSpacer />
        <Container className="midLayer glass">
          <h1 className="dropShadow"> {playerDetails.name} </h1>
          <Form
            onSubmit={handleSubmit}
            className="container justify-content-center"
          >
            <Container>
              <h2 className="dropShadow">Your practice routine</h2>
              <hr></hr>
              <h4 className="dropShadow">Your Collections</h4>
              <Row>
                {playerDetails.program.collections.map((collection, i) => {
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
              <Form.Group
                as={Row}
                className="align-items-center dropShadow fs-3"
              >
                <Form.Label className="dropShadow">Exercises</Form.Label>
                <Row>
                  {playerDetails.program.exerciseDetails.map((details, i) => {
                    return (
                      <Col key={i} xs={12} sm={3}>
                        <ExerciseDetailsForm
                          i={i}
                          details={details}
                          collections={playerDetails.program.collections}
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
                    value={playerDetails.program.rounds}
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
  }
};

export default UserProfile;
