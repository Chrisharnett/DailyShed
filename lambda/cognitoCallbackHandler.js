import { getCognitoToken } from "../util/getCognitoToken.js";
import { getCognitoUserData } from "../util/getCognitoUserData.js";
import jwt from "jsonwebtoken";

const cognitoCallbackHandler = async (event) => {
  const { code } = event.queryStringParameters;

  try {
    const cognitoToken = await getCognitoToken({ code });
    const { id_token, access_token, refresh_token } = cognitoToken.data;
    const userCognitoData = await getCognitoUserData({ id_token });

    const { sub, email_verified } = userCognitoData;

    const token = jwt.sign(
      {
        id_token,
        refresh_token,
        access_token,
        sub,
        email_verified,
      },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );

    // Include CORS headers in the response
    return {
      statusCode: 302,
      headers: {
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Origin": "*", // Allow all origins, or set it to "http://localhost:3000"
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        Location: `http://localhost:3000/?token=${token}`,
      },
      body: null,
    };
  } catch (error) {
    console.error("Error during Cognito callback:", error);

    // Return a 500 error response with CORS headers
    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
      },
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};

module.exports = { cognitoCallbackHandler };
