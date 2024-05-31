import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import ProgramCard from "../components/ProgramCard";
import ProgramBuilderCard from "../components/ProgramBuilderCard";
import SuccessModal from "../components/SuccessModal";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";

// A program has scaleMode, rhythmCollection, primaryCollection, tonicSequence, instrument.

const Programs = ({ user }) => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");
  const [userPrograms, setUserPrograms] = useState(null);
  const [rhythmCollections, setRhythmCollections] = useState(null);
  const [scalePatternPrograms, setScalePatternPrograms] = useState(null);
  const [tonicSequences, setTonicSequences] = useState(null);
  const [instruments, setInstruments] = useState(null);
  const [gotWhatINeed, setGotWhatINeed] = useState(false);

  useEffect(() => {
    const fetchProgramData = async () => {
      try {
        const programResponse = await axios.post(
          `/api/getProgramData/${user.sub}`
        );
        const {
          userPrograms,
          rhythmCollections,
          scalePatternPrograms,
          tonicSequences,
          instruments,
        } = programResponse.data;
        setUserPrograms(userPrograms);
        setRhythmCollections(rhythmCollections);
        setScalePatternPrograms(scalePatternPrograms);
        setTonicSequences(tonicSequences);
        setInstruments(instruments);
        setGotWhatINeed(true);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchProgramData();
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

  if (!gotWhatINeed) {
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
          <h1 className="dropShadow"> {userPrograms.userName} </h1>
          <Form
            onSubmit={handleSubmit}
            className="container justify-content-center"
          >
            <Container>
              <h2 className="dropShadow">Programs</h2>

              <hr></hr>
              <h4 className="dropShadow">Your Programs</h4>
              <Row>
                {userPrograms.map((program, i) => {
                  return (
                    <Col key={i} className="mb-2" xs={12} sm={4}>
                      <ProgramCard i={i} program={program} />
                    </Col>
                  );
                })}
              </Row>
              <hr></hr>
              {/* <Col className="mb-2" xs={12} sm={4}>
                <ProgramBuilderCard />
              </Col> */}
              <hr></hr>
              <Button variant="primary" type="submit" className="mt-2">
                Add Program
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

export default Programs;
