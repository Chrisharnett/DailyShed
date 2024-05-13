import axios from "axios";
import { logExercise } from "../commands/flaskRoutes.js";

export const logExerciseRoute = {
  path: "/api/logExercise",
  method: "post",
  handler: async (req, res) => {
    const exerciseEntry = req.body;

    try {
      const response = await axios.post(logExercise, exerciseEntry, {
        headers: { "Content-Type": "application/json" },
      });
      if (response.status === 200) {
        res.status(200).json(response.data);
      } else {
        res.status(500).json({ error: "Exercise logging failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
