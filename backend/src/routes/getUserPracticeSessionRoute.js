import axios from "axios";
import { getUserPracticeSession } from "../commands/flaskRoutes.js";

export const getUserPracticeSessionRoute = {
  path: "/api/getUserPracticeSession/:sub",
  method: "post",
  handler: async (req, res) => {
    const sub = req.params.sub;

    try {
      const response = await axios.post(
        getUserPracticeSession,
        { sub },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.practiceSession);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
