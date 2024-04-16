import { useState, useEffect } from "react";
import axios from "axios";
import { useToken } from "./useToken";

const useUser = () => {
  const [token] = useToken();
  const [user, setUser] = useState(null);
  const [playerDetails, setPlayerDetails] = useState(null);

  const getPayloadFromToken = (token) => {
    const encodedPayload = token.split(".")[1];
    return JSON.parse(atob(encodedPayload));
  };

  // const [user, setUser] = useState(() => {
  //   if (!token) {
  //     return null;
  //   } else {
  //     return getPayloadFromToken(token);
  //   }
  // });

  useEffect(() => {
    if (!token) {
      setUser(null);
      setPlayerDetails(null);
    } else {
      const newUser = getPayloadFromToken(token);
      setUser(newUser);
      fetchPlayerDetails(newUser.sub);
    }
  }, [token]);

  const fetchPlayerDetails = async (sub) => {
    try {
      const response = await axios.get(`/api/getUserData/${sub}`);
      setPlayerDetails(response.data.userData);
    } catch (error) {
      console.error("Error fetching player data: ", error);
      setPlayerDetails({
        name: "",
        email: "",
        exerciseMetadata: [],
        previousSet: [],
        program: {},
      });
    }
  };

  const updatePlayerDetails = async (newDetails) => {
    try {
      await axios.post("/api/updatePlayerDetails", newDetails);
      setPlayerDetails(newDetails);
    } catch (error) {
      console.error("Error updating player details:", error);
    }
  };

  return { user, playerDetails, updatePlayerDetails };
};

export default useUser;
