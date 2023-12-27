import jwt from "jsonwebtoken";
import { getCognitoToken } from "../util/getCognitoToken.js";

export const cognitoCallbackRoute = {
  path: "/api/auth/cognito/callback",
  method: "get",
  handler: async (req, res) => {
    const { code } = req.query;

    try {
      const cognitoToken = await getCognitoToken({ code });
      const { id_token, access_token, refresh_token } = cognitoToken.data;

      // Optionally: Validate ID token and extract user information

      // Create your JWT token
      const customToken = jwt.sign(
        {
          // Include necessary claims
          // e.g., userID, email, etc. extracted from the Cognito ID token
        },
        process.env.JWT_SECRET,
        { expiresIn: "1h" }
      );

      res.redirect(`http://localhost:3000/?token=${customToken}`);
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
    // jwt.sign(
    //   {
    //     userID,
    //     is_verified,
    //     email,
    //     name,
    //     max_properties,
    //     access_token,
    //     id_token,
    //     refresh_token,
    //     oauthId: oauthUserInfo.id,
    //   },
    //   process.env.JWT_SECRET,
    //   (err, token) => {
    //     if (err) return res.sendStatus(500);
    //     // res.redirect(`http://localhost:3000/?token=${token}`);

    //     res.redirect(`http://localhost:3000/?token=${token}`);
    //   }
    // );
    res.redirect(`http://localhost:3000/`);
  },
};
