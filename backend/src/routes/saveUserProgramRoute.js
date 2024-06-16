import axios from "axios";
import { saveUserProgram } from "../commands/flaskRoutes.js";

export const saveUserProgramRoute = {
  path: "/api/saveUserProgram",
  method: "post",
  handler: async (req, res) => {
    const program = req.body.program;

    try {
      const response = await axios.post(
        saveUserProgram,
        { program },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        res.status(200).json(response.data.userPrograms);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
