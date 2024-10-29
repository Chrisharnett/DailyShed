import { createContext, useState } from "react";
import PropTypes from "prop-types";

const RoutineContext = createContext();

const RoutineProvider = ({ children }) => {
  const [routine, setRoutine] = useState({ theme: "", time: "" });

  return (
    <RoutineContext.Provider value={{ routine, setRoutine }}>
      {children}
    </RoutineContext.Provider>
  );
};

RoutineProvider.propTypes = {
  children: PropTypes.node,
};

export default RoutineProvider;

export { RoutineContext };
