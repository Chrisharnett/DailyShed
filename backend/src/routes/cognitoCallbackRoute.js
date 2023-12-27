import jwt from "jsonwebtoken";
import { getCognitoToken } from "../util/getCognitoToken.js";
import { getCognitoUserData } from "../util/getCognitoUserData.js";

export const cognitoCallbackRoute = {
  path: "/api/auth/cognito/callback",
  method: "get",
  handler: async (req, res) => {
    const { code } = req.query;

    try {
      const cognitoToken = await getCognitoToken({ code });
      const { id_token, access_token, refresh_token } = cognitoToken.data;
      const userData = await getCognitoUserData({ id_token });

      const { sub, email, email_verified } = userData;
      const name = userData["cognito:username"];

      const token = jwt.sign(
        {
          id_token,
          refresh_token,
          access_token,
          sub,
          name,
          email,
          email_verified,
        },
        process.env.JWT_SECRET,
        { expiresIn: "1h" }
      );

      res.redirect(`http://localhost:3000/?token=${token}`);
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
