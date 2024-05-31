import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";
import { generateSetRoute } from "./generateSetRoute.js";
import { getUserDataRoute } from "./getUserDataRoute.js";
import { updateUserDataRoute } from "./updateUserDataRoute.js";
import { logExerciseRoute } from "./logExerciseRoute.js";
import { getUserJournalRoute } from "./getUserJournalRoute.js";
import { getUserPracticeSessionRoute } from "./getUserPracticeSessionRoute.js";
import { getUserProgramsRoute } from "./getUserProgramsRoute.js";
import { getScaleModesRoute } from "./getScaleModesRoute.js";
import { getRhythmOptionsRoute } from "./getRhythmOptionsRoute.js";
import { getProgramDataRoute } from "./getProgramDataRoute.js";

export const routes = [
  getProgramDataRoute,
  getRhythmOptionsRoute,
  getScaleModesRoute,
  getUserProgramsRoute,
  getUserPracticeSessionRoute,
  getUserJournalRoute,
  updateUserDataRoute,
  getUserDataRoute,
  generateSetRoute,
  getCognitoURLRoute,
  cognitoCallbackRoute,
  generateSetRoute,
  logExerciseRoute,
];
