import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useToken } from "./useToken";
import { useUserContext } from "./useUserContext";

const Callback = () => {
  const [, saveToken] = useToken();
  const { saveToken: saveUserToken, setUser } = useUserContext();
  const [codeProcessed, setCodeProcessed] = useState(false);
  const [tokenSaved, setTokenSaved] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (code && !codeProcessed) {
      exchangeCodeForTokens(code);
      setCodeProcessed(true);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [codeProcessed]);

  useEffect(() => {
    if (tokenSaved) {
      navigate("/");
    }
  }, [tokenSaved, navigate]);

  const exchangeCodeForTokens = async (code) => {
    const COGNITO_DOMAIN = `${import.meta.env.VITE_COGNITO_DOMAIN}`;
    const CLIENT_ID = `${import.meta.env.VITE_COGNITO_CLIENT_ID}`;
    const REDIRECT_URI = `${import.meta.env.VITE_COGNITO_CALLBACK}`;

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

      saveToken(response.data);
      const id_token = response.data.id_token;
      const user = getUserFromToken(id_token);
      setUser(user);

      setTokenSaved(true);
    } catch (error) {
      console.error("Error exchanging code for tokens:", error);
    }
  };

  const getUserFromToken = (token) => {
    try {
      const parts = token.split(".");
      if (parts.length !== 3) {
        throw new Error("Invalid token format");
      }

      const encodedPayload = parts[1];
      const decodedPayload = atob(encodedPayload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error("Error decoding token:", error);
      return null;
    }
  };

  return <div>Loading...</div>;
};

export default Callback;
