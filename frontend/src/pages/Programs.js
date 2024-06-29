import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import ProgramCard from "../components/ProgramCard";
import ProgramBuilderCard from "../components/ProgramBuilderCard";
import SuccessModal from "../components/SuccessModal";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";

const Programs = ({ user }) => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");
  const [userPrograms, setUserPrograms] = useState({
    userName: "",
    programs: [],
  });
  const [rhythmCollections, setRhythmCollections] = useState(null);
  const [scalePatternPrograms, setScalePatternPrograms] = useState(null);
  const [tonicSequences, setTonicSequences] = useState(null);
  const [instruments, setInstruments] = useState(null);
  const [modes, setModes] = useState(null);
  const [gotWhatINeed, setGotWhatINeed] = useState(false);

  useEffect(() => {
    const fetchProgramData = async () => {
      try {
        const programResponse = await axios.post(
          `/api/getProgramData/${user.sub}`
        );
        handleProgramUpdate(programResponse.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchProgramData();
    }
  }, [user]);

  const handleProgramUpdate = async (updatedPrograms) => {
    const {
      userPrograms,
      rhythmCollections,
      scalePatternPrograms,
      tonicSequences,
      instruments,
      modes,
    } = updatedPrograms;
    setUserPrograms(userPrograms);
    setRhythmCollections(rhythmCollections);
    setScalePatternPrograms(scalePatternPrograms);
    setTonicSequences(tonicSequences);
    setInstruments(instruments);
    setModes(modes);
    setGotWhatINeed(true);
  };

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

  if (userPrograms.programs.length < 1) {
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
                {userPrograms.programs.length > 0 ? (
                  userPrograms.programs.map((program, i) => (
                    <Col key={i} className="mb-2" xs={12} sm={4}>
                      <ProgramCard i={i} user={user} program={program} />
                    </Col>
                  ))
                ) : (
                  <p>Create a new program first</p>
                )}
              </Row>
              <hr></hr>
              <Col className="mb-2" xs={12} sm={4}>
                <ProgramBuilderCard
                  user={user}
                  rhythmCollections={rhythmCollections}
                  scalePatternPrograms={scalePatternPrograms}
                  tonicSequences={tonicSequences}
                  instruments={instruments}
                  modes={modes}
                  userDefaultInstrument={
                    userPrograms.programs[0].instrumentName
                  }
                  setMessage={setMessage}
                  setOpenSuccessMessage={setOpenSuccessMessage}
                  handleProgramUpdate={handleProgramUpdate}
                />
              </Col>
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
