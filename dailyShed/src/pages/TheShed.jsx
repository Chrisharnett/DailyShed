// Desc: This is the main page for the dailyShed app. It will use the Routine Builder for users to set up their practice routine and display their practice routine.
import { useEffect, useState } from "react";
import LoadingScreen from "../components/common/LoadingScreen";
import GlassContainer from "../components/common/GlassContainer";
import PracticeRoutine from "../components/PracticeRoutine/PracticeRoutine";
import RoutineBuilder from "../components/RoutineBuilder/RoutineBuilder";
import PracticeDebrief from "../components/PracticeDebrief/PracticeDebrief";

const TheShed = () => {
  const [title, setTitle] = useState("");
  const [subtitle, setSubtitle] = useState("");
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    switch (currentStep) {
      case 1:
        setSubtitle("Create Your Practice Routine");
        break;
      case 2:
        setSubtitle("Practice time");
        break;
      case 3:
        setSubtitle("Excellent work!");
        break;
      default:
        setSubtitle("Just a moment");
        break;
    }
  }, [currentStep]);

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <RoutineBuilder
            onNext={() => setCurrentStep(2)}
            setSubtitle={setTitle}
          />
        );
      case 2:
        setTitle("Practice time");
        return (
          <PracticeRoutine
            onNext={() => setCurrentStep(2)}
            setSubtitle={setTitle}
          />
        );
      case 3:
        setTitle("Excellent work!");
        return (
          <PracticeDebrief
            onNext={() => setCurrentStep(2)}
            setSubtitle={setTitle}
          />
        );
      default:
        return <LoadingScreen message="Just a moment" />;
    }
  };

  return (
    <>
      <GlassContainer
        title={title}
        subtitle={subtitle}
        startAnimation={true}
        // cueNextAnimation={setCueExerciseCard}
      >
        {renderStep()}
      </GlassContainer>
    </>
  );
};

export default TheShed;
