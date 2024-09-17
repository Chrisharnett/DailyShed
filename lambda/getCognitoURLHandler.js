const getCognitoURLHandler = async (event) => {
  try {
    const url = `${process.env.COGNITO_DOMAIN}/login?response_type=code&client_id=${process.env.COGNITO_CLIENT_ID}&redirect_uri=${process.env.COGNITO_CALLBACK}`;

    // Include CORS headers in the response
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
      },
      body: JSON.stringify({ url }),
    };
  } catch (error) {
    console.error("Error getting Cognito URL:", error);

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

module.exports = { getCognitoURLHandler };
