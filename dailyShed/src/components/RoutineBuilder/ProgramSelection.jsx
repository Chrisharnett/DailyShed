import PropTypes from "prop-types";
import AnimatedButton from "../common/AnimatedButton";
import { useEffect } from "react";
import { getRoutine } from "../../util/flaskRoutes";
import axios from "axios";
import { useState } from "react";
import { useUserContext } from "../../auth/useUserContext";
import { RoutineContext } from "../../context/RoutineContext";
import ProgramFocus from "./ProgramFocus";
import { Container } from "react-bootstrap";

const ProgramSelection = ({ onNext, setSubtitle }) => {
  const [session, setSession] = useState(null);
  const { user } = useUserContext();

  useEffect(() => {
    const fetchPracticeSession = async () => {
      try {
        const sessionResponse = await axios.get(`${getRoutine}/${user.sub}`);
        setSession(sessionResponse.data.session);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchPracticeSession();
    }
  }, [user]);

  const handleThemeSelect = (theme) => {
    onNext(theme);
  };

  useEffect(() => {
    setSubtitle("What would you like to focus on?");
  }, [setSubtitle]);

  return (
    <Container>
      <h2>Programs</h2>
      {session && <ProgramFocus programs={session} />}
      <hr></hr>
      <Container fluid>
        <AnimatedButton
          handleOnClick={() => handleThemeSelect("Done")}
          buttonText={"Done"}
        />
      </Container>
    </Container>
  );
};

ProgramSelection.propTypes = {
  onNext: PropTypes.func.isRequired,
  setSubtitle: PropTypes.func.isRequired,
};

export default ProgramSelection;
