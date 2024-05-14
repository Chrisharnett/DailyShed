import axios from "axios";
import { getScaleModes } from "../commands/flaskRoutes.js";

export const getScaleModesRoute = {
  path: "/api/getScaleModes/",
  method: "get",
  handler: async (req, res) => {
    try {
      const response = await axios.get(getScaleModes);

      if (response.status === 200) {
        res.status(200).json(response.data.modes);
      } else {
        res.status(500).json({ error: "Request failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
