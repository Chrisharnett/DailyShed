import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";
import { generateSetRoute } from "./generateSetRoute.js";
import { getUserDataRoute } from "./getUserDataRoute.js";
import { updateUserDataRoute } from "./updateUserDataRoute.js";
import { logExerciseRoute } from "./logExerciseRoute.js";
import { getUserJournalRoute } from "./getUserJournalRoute.js";

export const routes = [
  getUserJournalRoute,
  updateUserDataRoute,
  getUserDataRoute,
  generateSetRoute,
  getCognitoURLRoute,
  cognitoCallbackRoute,
  generateSetRoute,
  logExerciseRoute,
];
