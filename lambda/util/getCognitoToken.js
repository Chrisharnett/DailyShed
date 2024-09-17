import axios from "axios";

export const getCognitoToken = async ({ code }) => {
  // Exchange code for tokens
  const tokenResponse = await axios.post(
    `${process.env.COGNITO_DOMAIN}/oauth2/token`,
    new URLSearchParams({
      grant_type: "authorization_code",
      client_id: process.env.COGNITO_CLIENT_ID,
      code: code,
      redirect_uri: process.env.COGNITO_CALLBACK,
    }),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  return tokenResponse;
};
