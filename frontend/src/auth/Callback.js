import { useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useToken } from "./useToken";

const Callback = () => {
  const [, setToken] = useToken();
  const navigate = useNavigate();
  useEffect(() => {
    const code = new URL(window.location.href).searchParams.get("code");
    if (code) {
      exchangeCodeForTokens(code);
    }
  }, []);

  const exchangeCodeForTokens = async (code) => {
    const COGNITO_DOMAIN = `${process.env.REACT_APP_COGNITO_DOMAIN}`;
    const CLIENT_ID = `${process.env.REACT_APP_COGNITO_CLIENT_ID}`;
    const REDIRECT_URI = `${process.env.REACT_APP_COGNITO_CALLBACK}`;

    const body = new URLSearchParams({
      grant_type: "authorization_code",
      client_id: CLIENT_ID,
      code: code,
      redirect_uri: REDIRECT_URI,
    });

    try {
      const response = await axios.post(
        `${COGNITO_DOMAIN}/oauth2/token`,
        body,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      console.log("Tokens:", response.data);
      // Save tokens in local storage or session storage
      setToken(response.data.id_token);
      sessionStorage.setItem("access_token", response.data.access_token);
      sessionStorage.setItem("refresh_token", response.data.refresh_token);

      navigate("/");
    } catch (error) {
      console.error("Error exchanging code for tokens:", error);
    }
  };

  return <div>Loading...</div>;
};

export default Callback;
