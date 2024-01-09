import jwt from "jsonwebtoken";
import { putUserData } from "../commands/userCommands.js";

export const updateUserDataRoute = {
  path: "/api/updateUserData/",
  method: "post",
  handler: async (req, res) => {
    const userData = req.body;

    try {
      const response = await putUserData(userData);
      res.status(200).json({ response });
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
