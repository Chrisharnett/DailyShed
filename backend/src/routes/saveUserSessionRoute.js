import axios from "axios";
import { saveUserSession } from "../commands/flaskRoutes.js";

export const saveUserSessionRoute = {
  path: "/api/saveUserSession",
  method: "post",
  handler: async (req, res) => {
    const session = req.body;

    try {
      const response = await axios.post(
        saveUserSession,
        { session: session },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.userSession);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
