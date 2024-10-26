import { useState } from "react";

export const useToken = () => {
  // Retrieve the token from sessionStorage
  const getToken = () => {
    try {
      const tokenString = sessionStorage.getItem("authToken");

      // Return null if tokenString is null or is the string "undefined"
      if (!tokenString || tokenString === "undefined") {
        return null;
      }

      // Parse the token if it exists and is not "undefined"
      return JSON.parse(tokenString);
    } catch (error) {
      console.error("Failed to parse token:", error);
      return null;
    }
  };

  // Set initial token state
  const [token, setToken] = useState(getToken());

  // Save the token in sessionStorage and update state
  const saveToken = (newToken) => {
    if (newToken !== undefined && newToken !== null) {
      sessionStorage.setItem("authToken", JSON.stringify(newToken));
      setToken(newToken);
    }
  };

  // Remove the token from sessionStorage and update state
  const removeToken = () => {
    sessionStorage.removeItem("authToken");
    setToken(null);
  };

  return [token, saveToken, removeToken];
};
