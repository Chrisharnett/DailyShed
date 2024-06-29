import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import AddButton from "../components/AddButton";
import IntervalDetails from "../components/IntervalDetails";
import SuccessModal from "../components/SuccessModal";
import AddIntervalModal from "../components/AddIntervalModal";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";

const UserProfile = ({ user }) => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");
  const [practiceSession, setPracticeSession] = useState(null);
  const [userPrograms, setUserPrograms] = useState(null);
  const [scaleModes, setScaleModes] = useState(null);
  const [rhythmOptions, setRhythmOptions] = useState(null);
  const [openNewInterval, setOpenNewInterval] = useState(false);

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

  const updatePlayerSession = async (newSession) => {
    try {
      await axios.post(`/api/saveUserSession`, newSession);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await updatePlayerSession({
        sub: user.sub,
        practiceSession: practiceSession,
      });
      setMessage("Routine Saved!");
      setOpenSuccessMessage(true);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const handleRoundsChange = (event) => {
    const newRounds = parseInt(event.target.value);
    setPracticeSession({ ...practiceSession, rounds: newRounds });
  };

  const handleDetailsChange = (index, updatedDetails) => {
    const newExerciseDetails = [...practiceSession.intervals];
    newExerciseDetails[index] = updatedDetails;

    setPracticeSession({
      ...practiceSession,
      intervals: newExerciseDetails,
    });
  };

  const removeInterval = (index) => {
    const newExerciseDetails = practiceSession.intervals.filter(
      (interval, i) => i !== index
    );
    setPracticeSession({
      ...practiceSession,
      intervals: newExerciseDetails,
    });
  };

  const addIntervalToSession = (newInterval) => {
    setPracticeSession((prevState) => ({
      ...prevState,
      intervals: [...prevState.intervals, newInterval],
    }));
  };

  const handleAddInterval = (e) => {
    e.preventDefault();
    setOpenNewInterval(true);
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
              <Form.Group
                as={Row}
                className="align-items-center dropShadow fs-3"
              >
                <h1>Exercises</h1>
                <Row>
                  {practiceSession.intervals.map((interval, i) => {
                    return (
                      <Col key={i} xs={12} sm={3}>
                        <IntervalDetails
                          i={i}
                          interval={interval}
                          programs={userPrograms.programs}
                          removeInterval={removeInterval}
                          userPrograms={userPrograms}
                          onDetailsChange={(updatedDetails) =>
                            handleDetailsChange(i, updatedDetails)
                          }
                        />
                      </Col>
                    );
                  })}
                  <Col xs="auto">
                    <AddButton onClick={handleAddInterval} />
                  </Col>
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
        <AddIntervalModal
          show={openNewInterval}
          setShow={setOpenNewInterval}
          programs={userPrograms.programs}
          addIntervalToSession={addIntervalToSession}
        />
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
