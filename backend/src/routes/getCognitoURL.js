import "dotenv/config";

export const getCognitoURLRoute = {
  path: "/api/auth/cognito/url",
  method: "get",
  handler: (req, res) => {
    const url = `${process.env.COGNITO_DOMAIN}/login?response_type=code&client_id=${process.env.AWS_CLIENT_ID}&redirect_uri=${process.env.COGNITO_CALLBACK}`;
    res.status(200).json({ url });
  },
};
