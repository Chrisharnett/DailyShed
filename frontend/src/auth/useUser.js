import { useState, useEffect } from "react";
import { useToken } from "./useToken";

const useUser = () => {
  const [token] = useToken();
  const [user, setUser] = useState(null);

  const getPayloadFromToken = (token) => {
    const encodedPayload = token.split(".")[1];
    return JSON.parse(atob(encodedPayload));
  };

  useEffect(() => {
    if (!token) {
      setUser(null);
    } else {
      const newUser = getPayloadFromToken(token);
      setUser(newUser);
    }
  }, [token]);

  return { user };
};

export default useUser;
