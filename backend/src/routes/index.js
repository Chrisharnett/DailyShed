import { signUpRoute } from "./signUpRoute.js";
import { loginRoute } from "./loginRoute.js";
import { testRoute } from "./testRoute.js";
import { updateUserInfoRoute } from "./updateUserInfoRoute.js";
import { testEmailRoute } from "./testEmailRoute.js";
import { verifyEmailRoute } from "./verifyEmailRoute.js";
import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";
import { generateSetRoute } from "./generateSetRoute.js";
import { flaskTestRoute } from "./flaskTestRoute.js";
import { getUserDataRoute } from "./getUserDataRoute.js";

export const routes = [
  getUserDataRoute,
  flaskTestRoute,
  generateSetRoute,
  getCognitoURLRoute,
  cognitoCallbackRoute,
  testRoute,
  signUpRoute,
  loginRoute,
  updateUserInfoRoute,
  testEmailRoute,
  verifyEmailRoute,
];
