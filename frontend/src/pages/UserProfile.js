import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import ExerciseDetailsForm from "../components/ExerciseDetailsForm";
import SuccessModal from "../components/SuccessModal";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";

const UserProfile = ({ user }) => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");
  const [practiceSession, setPracticeSession] = useState(null);
  const [userPrograms, setUserPrograms] = useState(null);
  const [scaleModes, setScaleModes] = useState(null);
  const [rhythmOptions, setRhythmOptions] = useState(null);

  useEffect(() => {
    const fetchPracticeSession = async () => {
      try {
        const sessionResponse = await axios.post(
          `/api/getUserPracticeSession/${user.sub}`
        );
        setPracticeSession(sessionResponse.data);

        const programResponse = await axios.post(
          `/api/getUserPrograms/${user.sub}`
        );
        setUserPrograms(programResponse.data);

        const scaleModesResponse = await axios.get("/api/getScaleModes");
        setScaleModes(scaleModesResponse.data);

        const rhythmOptionsResponse = await axios.post(
          `/api/getRhythmOptions/${user.sub}`
        );
        setRhythmOptions(rhythmOptionsResponse.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchPracticeSession();
    }
  }, [user]);

  const handleSubmit = async (event) => {
    // event.preventDefault();
    // const newUserData = { ...playerDetails };
    // try {
    //   await updatePlayerDetails(newUserData);
    //   setMessage("Routine Saved!");
    //   setOpenSuccessMessage(true);
    // } catch (error) {
    //   console.error("Error: ", error);
    // }
  };

  const handleRoundsChange = (event) => {
    // const newRounds = parseInt(event.target.value);
    // updatePlayerDetails({
    //   ...playerDetails,
    //   program: {
    //     ...playerDetails.program,
    //     rounds: newRounds,
    //   },
    // });
  };

  const handleDetailsChange = (index) => {
    // const newExerciseDetails = [...playerDetails.program.exerciseDetails];
    // newExerciseDetails[index] = updatedDetails;
    // updatePlayerDetails({
    //   ...playerDetails,
    //   program: {
    //     ...playerDetails.program,
    //     exerciseDetails: newExerciseDetails,
    //   },
    // });
  };

  if (!userPrograms || !practiceSession || !scaleModes || !rhythmOptions) {
    return (
      <>
        <TopSpacer />
        <p>Loading...</p>;
      </>
    );
  } else {
    return (
      <>
        <TopSpacer />
        <Container className="midLayer glass">
          <h1 className="dropShadow"> {userPrograms.programs.userName} </h1>
          <Form
            onSubmit={handleSubmit}
            className="container justify-content-center"
          >
            <Container>
              <h2 className="dropShadow">Your practice routine</h2>
              <hr></hr>
              {/* TODO: Add the ability to change the number of Exercises */}
              {/* TODO: Allow Custom Exercises */}
              <Form.Group
                as={Row}
                className="align-items-center dropShadow fs-3"
              >
                <Form.Label className="dropShadow">Exercises</Form.Label>
                <Row>
                  {practiceSession.intervals.map((interval, i) => {
                    return (
                      <Col key={i} xs={12} sm={3}>
                        <ExerciseDetailsForm
                          i={i}
                          interval={interval}
                          programs={userPrograms.programs}
                          scaleModes={scaleModes}
                          rhythmOptions={rhythmOptions}
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
                    value={practiceSession.rounds}
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
