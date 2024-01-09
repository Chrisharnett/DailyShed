import jwt from "jsonwebtoken";
import { getCognitoToken } from "../util/getCognitoToken.js";
import { getCognitoUserData } from "../util/getCognitoUserData.js";
import { getUserData } from "../commands/userCommands.js";

export const cognitoCallbackRoute = {
  path: "/api/auth/cognito/callback",
  method: "get",
  handler: async (req, res) => {
    const { code } = req.query;

    try {
      const cognitoToken = await getCognitoToken({ code });
      const { id_token, access_token, refresh_token } = cognitoToken.data;
      const userCognitoData = await getCognitoUserData({ id_token });

      const { sub, email, email_verified } = userCognitoData;

      const token = jwt.sign(
        {
          id_token,
          refresh_token,
          access_token,
          sub,
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
