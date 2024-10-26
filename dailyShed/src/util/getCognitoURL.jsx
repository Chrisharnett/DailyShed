export const getCognitoURL = `${
  import.meta.env.VITE_COGNITO_DOMAIN
}/login?response_type=code&client_id=${
  import.meta.env.VITE_COGNITO_CLIENT_ID
}&redirect_uri=${import.meta.env.VITE_COGNITO_CALLBACK}`;
