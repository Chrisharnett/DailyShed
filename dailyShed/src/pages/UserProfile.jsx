import { Form, Row, Col, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import AddButton from "../components/AddButton";
import IntervalDetails from "../components/IntervalDetails";
import SuccessModal from "../components/SuccessModal";
import AddIntervalModal from "../components/AddIntervalModal";
import {
  getUserPracticeSession,
  getScaleModes,
  getRhythmOptions,
  saveUserSession,
  getUserPrograms,
} from "../util/flaskRoutes";
import axios from "axios";
import { useUserContext } from "../auth/useUserContext";
import GlassContainer from "../components/GlassContainer";
import LoadingScreen from "../components/LoadingScreen";
import { motion } from "framer-motion";
import {
  itemSpellerVariantDefaults,
  containerSpellerVariantDefaults,
} from "../config/animationConfig";
import AnimatedButton from "../components/AnimatedButton";

const UserProfile = () => {
  const [openSuccessMessage, setOpenSuccessMessage] = useState(false);
  const [message, setMessage] = useState("");
  const [practiceSession, setPracticeSession] = useState(null);
  const [userPrograms, setUserPrograms] = useState(null);
  const [scaleModes, setScaleModes] = useState(null);
  const [rhythmOptions, setRhythmOptions] = useState(null);
  const [openNewInterval, setOpenNewInterval] = useState(false);
  const [cueExercises, setCueExercises] = useState(false);
  const [cueNextIntervalAnimation, setCueNextIntervalAnimation] = useState([]);
  const { user } = useUserContext();

  // useEffect(() => {
  //   if (practiceSession?.intervals) {
  //     const initialAnimations = practiceSession.intervals.map(() => false);
  //     setCueNextIntervalAnimation(initialAnimations);
  //   }
  // }, [practiceSession?.intervals]);

  useEffect(() => {
    const fetchPracticeSession = async () => {
      try {
        const sessionResponse = await axios.post(
          `${getUserPracticeSession}/${user.sub}`
        );
        setPracticeSession(sessionResponse.data.practiceSession);

        const programResponse = await axios.post(
          `${getUserPrograms}/${user.sub}`
        );
        setUserPrograms(programResponse.data.programs);

        const scaleModesResponse = await axios.get(`${getScaleModes}`);
        setScaleModes(scaleModesResponse.data.modes);

        const rhythmOptionsResponse = await axios.post(
          `${getRhythmOptions}/${user.sub}`
        );
        setRhythmOptions(rhythmOptionsResponse.data.rhythmPatternOptions);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchPracticeSession();
    }
  }, [user]);

  // useEffect(() => {
  //   if (cueExercises && cueNextIntervalAnimation.length > 0) {
  //     setCueNextIntervalAnimation((prevAnimations) => {
  //       const updatedAnimations = [...prevAnimations];
  //       updatedAnimations[0] = true;
  //       return updatedAnimations;
  //     });
  //   }
  // }, [cueExercises, cueNextIntervalAnimation]);

  const updatePlayerSession = async (newSession) => {
    try {
      await axios.post(`${saveUserSession}`, newSession);
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

  // const cueNextAnimation = (currentIndex) => {
  //   setCueNextIntervalAnimation((prevAnimations) => {
  //     const updatedAnimations = [...prevAnimations];
  //     if (currentIndex + 1 < updatedAnimations.length) {
  //       updatedAnimations[currentIndex + 1] = true;
  //     }
  //     return updatedAnimations;
  //   });
  // };

  if (!userPrograms || !practiceSession || !scaleModes || !rhythmOptions) {
    return <LoadingScreen />;
  } else {
    return (
      <>
        <GlassContainer
          title={userPrograms.userName}
          subtitle="Create your practice routine"
          startAnimation={true}
          cueNextAnimation={setCueExercises}
        >
          <Form
            onSubmit={handleSubmit}
            className="container justify-content-center"
          >
            <hr></hr>
            <Form.Group as={Row} className="align-items-center dropShadow ">
              <motion.span
                className=""
                variants={containerSpellerVariantDefaults}
                initial="hidden"
                animate={cueExercises ? "visible" : "hidden"}
                // onAnimationComplete={handleAnimationComplete}
              >
                {practiceSession.intervals.map((interval, i) => {
                  return (
                    <Row key={i}>
                      <motion.div variants={itemSpellerVariantDefaults}>
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
                      </motion.div>
                    </Row>
                  );
                })}
              </motion.span>
              <Col xs="auto">
                <AddButton onClick={handleAddInterval} />
              </Col>
              {/* </Row> */}
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
            <AnimatedButton
              buttonText="Save Routine"
              variant="primary"
              className="mt-2"
              handleOnClick={handleSubmit}
            />
            {/* <Button variant="primary" type="submit" className="mt-2">
              Save Routine
            </Button> */}
          </Form>
        </GlassContainer>
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
      </>
    );
  }
};

export default UserProfile;
