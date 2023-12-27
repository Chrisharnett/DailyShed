import { signUpRoute } from "./signUpRoute.js";
import { loginRoute } from "./loginRoute.js";
import { testRoute } from "./testRoute.js";
import { updateUserInfoRoute } from "./updateUserInfoRoute.js";
import { testEmailRoute } from "./testEmailRoute.js";
import { verifyEmailRoute } from "./verifyEmailRoute.js";
import { cognitoCallbackRoute } from "./cognitoCallbackRoute.js";
import { getCognitoURLRoute } from "./getCognitoURL.js";

export const routes = [
  getCognitoURLRoute,
  cognitoCallbackRoute,
  testRoute,
  signUpRoute,
  loginRoute,
  updateUserInfoRoute,
  testEmailRoute,
  verifyEmailRoute,
];
