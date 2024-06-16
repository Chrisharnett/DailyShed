import { getUserJournal } from "../commands/flaskRoutes.js";
import axios from "axios";

export const getUserJournalRoute = {
  path: "/api/getUserJournal/:sub",
  method: "post",
  handler: async (req, res) => {
    const sub = req.params.sub;
    try {
      const response = await axios.post(
        getUserJournal,
        { sub },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.userHistory);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
