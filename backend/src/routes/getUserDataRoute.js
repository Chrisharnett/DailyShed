import jwt from "jsonwebtoken";
import { getUserData } from "../commands/userCommands.js";

export const getUserDataRoute = {
  path: "/api/auth/getUserData/:sub",
  method: "get",
  handler: async (req, res) => {
    const sub = req.params.sub;

    try {
      const response = await getUserData(sub);
      const userData = response.Item;
      res.status(200).json({ userData });
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
