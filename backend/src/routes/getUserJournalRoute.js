import { getUserJournal } from "../commands/userCommands.js";

export const getUserJournalRoute = {
  path: "/api/getUserJournal/:sub",
  method: "get",
  handler: async (req, res) => {
    const sub = req.params.sub;
    try {
      const response = await getUserJournal(sub);
      const userData = response.Item;
      res.status(200).json({ userData });
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
