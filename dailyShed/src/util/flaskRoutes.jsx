const flaskURL =
  import.meta.env.VITE_NODE_ENV === "production"
    ? import.meta.env.VITE_FLASK_URL_PROD
    : import.meta.env.VITE_FLASK_URL_LOCAL;

export const setGenerator = `${flaskURL}/generateSet`;
export const logExercise = `${flaskURL}/logExercise`;
export const getUserPracticeSession = `${flaskURL}/getUserPracticeSession`;
export const getUserPrograms = `${flaskURL}/getUserPrograms`;
export const getScaleModes = `${flaskURL}/getScaleModes`;
export const getRhythmOptions = `${flaskURL}/getRhythmPatternOptions`;
export const getUserJournal = `${flaskURL}/userExerciseLog`;
export const getProgramData = `${flaskURL}/getProgramData`;
export const saveUserProgram = `${flaskURL}/addNewUserProgram`;
export const saveUserSession = `${flaskURL}/addNewUserSession`;
