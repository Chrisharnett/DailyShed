import { updatePreviousSet } from "../commands/userCommands.js";

export const updatePreviousSetRoute = {
  path: "/api/updatePreviousSet/",
  method: "post",
  handler: async (req, res) => {
    const { player, previousSet } = req.body;
    try {
      const response = await updatePreviousSet(player, previousSet);
      res.status(200).json({ response });
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
