import axios from "axios";
import { getUserPrograms } from "../commands/flaskRoutes.js";

export const getUserProgramsRoute = {
  path: "/api/getUserPrograms/:sub",
  method: "post",
  handler: async (req, res) => {
    const sub = req.params.sub;

    try {
      const response = await axios.post(
        getUserPrograms,
        { sub },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.programs);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
