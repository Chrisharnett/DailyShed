// src/hooks/useFetchRoutine.js
import { useEffect, useState } from "react";
import axios from "axios";
import { getRoutine } from "../util/flaskRoutes";

const useFetchRoutine = (sub) => {
  const [routine, setRoutine] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRoutine = async () => {
      try {
        const response = await axios.get(`${getRoutine}/${sub}`);
        setRoutine(response.data.session);
      } catch (error) {
        console.error("Error fetching routine:", error);
      } finally {
        setLoading(false);
      }
    };

    if (sub) {
      fetchRoutine();
    }
  }, [sub]);

  return { routine, loading, setRoutine };
};

export default useFetchRoutine;
