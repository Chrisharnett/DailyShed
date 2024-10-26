import { createContext, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useToken } from "./useToken";

// Creating UserContext
export const UserContext = createContext();

// Creating the UserProvider component
export const UserProvider = ({ children }) => {
  const [token, saveToken, removeToken] = useToken();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Function to extract payload from JWT token
  const getPayloadFromToken = (token) => {
    if (!token || typeof token !== "object") {
      return null;
    }

    const { id_token } = token;

    if (!id_token || typeof id_token !== "string") {
      return null;
    }

    try {
      const parts = id_token.split(".");
      if (parts.length !== 3) {
        return null;
      }

      const encodedPayload = parts[1];
      const decodedPayload = atob(encodedPayload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error("Error decoding token:", error);
      return null;
    }
  };

  const customSaveToken = (newToken) => {
    saveToken(newToken);
    if (newToken) {
      const userInfo = getPayloadFromToken(newToken);
      setUser(userInfo);
    } else {
      setUser(null);
    }
  };

  // Update user state whenever the token changes
  useEffect(() => {
    const storedToken =
      token || JSON.parse(sessionStorage.getItem("authToken"));
    if (storedToken) {
      const userInfo = getPayloadFromToken(token);
      setUser(userInfo);
    } else {
      setUser(null);
    }
    setLoading(false);
  }, [token]);

  return (
    <UserContext.Provider
      value={{
        user,
        setUser,
        saveToken: customSaveToken,
        removeToken,
        loading,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

UserProvider.propTypes = {
  children: PropTypes.node,
};
