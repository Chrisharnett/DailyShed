import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";
import { generateSetRoute } from "./generateSetRoute.js";
import { logExerciseRoute } from "./logExerciseRoute.js";
import { getUserJournalRoute } from "./getUserJournalRoute.js";
import { getUserPracticeSessionRoute } from "./getUserPracticeSessionRoute.js";
import { getUserProgramsRoute } from "./getUserProgramsRoute.js";
import { getScaleModesRoute } from "./getScaleModesRoute.js";
import { getRhythmOptionsRoute } from "./getRhythmOptionsRoute.js";
import { getProgramDataRoute } from "./getProgramDataRoute.js";
import { saveUserProgramRoute } from "./saveUserProgramRoute.js";
import { saveUserSessionRoute } from "./saveUserSessionRoute.js";

export const routes = [
  saveUserSessionRoute,
  saveUserProgramRoute,
  getProgramDataRoute,
  getRhythmOptionsRoute,
  getScaleModesRoute,
  getUserProgramsRoute,
  getUserPracticeSessionRoute,
  getUserJournalRoute,
  generateSetRoute,
  getCognitoURLRoute,
  cognitoCallbackRoute,
  generateSetRoute,
  logExerciseRoute,
];
