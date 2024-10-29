import { useEffect, useState, useContext } from "react";
import PropTypes from "prop-types";
import { RoutineContext } from "../../context/RoutineContext";
import ProgramSelection from "./ProgramSelection";
import TimeSelection from "./TimeSelection";
import RoutineSummary from "./RoutineSummary";
import { useUserContext } from "../../auth/useUserContext";
import useFetchRoutine from "../../hooks/useFetchRoutine";
import LoadingScreen from "../common/LoadingScreen";

const RoutineBuilder = ({ setSubtitle, onNext }) => {
  const { routine, setRoutine } = useContext(RoutineContext);
  const [currentStep, setCurrentStep] = useState(1);
  const { user } = useUserContext();
  const { routine: fetchedRoutine, loading } = useFetchRoutine(user.sub);

  useEffect(() => {
    if (fetchedRoutine) {
      setRoutine(fetchedRoutine);
    }
  }, []);

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <TimeSelection
            setSubtitle={setSubtitle}
            onNext={(time) => {
              setRoutine({ ...routine, time });
              setCurrentStep(2);
            }}
          />
        );
      case 2:
        return (
          <ProgramSelection
            setSubtitle={setSubtitle}
            onNext={(session) => {
              setRoutine({ ...routine, session });
              setCurrentStep(3);
            }}
          />
        );

      case 3:
        return (
          <RoutineSummary
            routine={routine}
            setSubtitle={setSubtitle}
            onConfirm={() => {
              setCurrentStep(4);
              onNext();
            }}
          />
        );
      default:
        return null;
    }
  };
  if (loading) {
    return <LoadingScreen message="Incoming" />;
  }
  return <div>{renderStep()}</div>;
};

RoutineBuilder.propTypes = {
  setSubtitle: PropTypes.func,
  onNext: PropTypes.func,
};

export default RoutineBuilder;
