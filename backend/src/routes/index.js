import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";
import { generateSetRoute } from "./generateSetRoute.js";
import { flaskTestRoute } from "./flaskTestRoute.js";
import { getUserDataRoute } from "./getUserDataRoute.js";
import { updateUserDataRoute } from "./updateUserDataRoute.js";
import { logExerciseRoute } from "./logExerciseRoute.js";

export const routes = [
  updateUserDataRoute,
  getUserDataRoute,
  flaskTestRoute,
  generateSetRoute,
  getCognitoURLRoute,
  cognitoCallbackRoute,
  generateSetRoute,
  logExerciseRoute,
];
