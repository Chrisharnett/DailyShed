import axios from "axios";
import { getProgramData } from "../commands/flaskRoutes.js";

export const getProgramDataRoute = {
  path: "/api/getProgramData/:sub",
  method: "post",
  handler: async (req, res) => {
    const sub = req.params.sub;

    try {
      const response = await axios.post(
        getProgramData,
        { sub },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.programData);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
