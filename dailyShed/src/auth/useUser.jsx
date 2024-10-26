import { useState, useEffect } from "react";
import { useToken } from "./useToken";

const useUser = () => {
  const [token, , removeToken] = useToken();

  // Function to extract payload from JWT token
  const getPayloadFromToken = (token) => {
    if (!token || typeof token !== "object") {
      console.error("Invalid token:", token);
      removeToken();
      return null;
    }

    const { id_token } = token;

    if (!id_token || typeof id_token !== "string") {
      console.error("Invalid or missing id_token:", id_token);
      removeToken();
      return null;
    }

    const parts = id_token.split(".");

    if (parts.length !== 3) {
      console.error("Token does not have the expected format:", id_token);
      removeToken();
      return null;
    }

    try {
      const encodedPayload = parts[1];
      const decodedPayload = atob(encodedPayload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error("Error decoding token:", id_token, error);
      removeToken();
      return null;
    }
  };

  // Initialize the user state from the token if it exists
  const [user, setUser] = useState(() => {
    return token ? getPayloadFromToken(token) : null;
  });

  // Update the user state when the token changes
  useEffect(() => {
    if (!token) {
      setUser(null);
    } else {
      setUser(getPayloadFromToken(token));
    }
  }, [token]);

  return user;
};

export default useUser;
