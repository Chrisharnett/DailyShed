import { getUserJournal } from "../commands/userCommands.js";

export const getUserJournalRoute = {
  path: "/api/getUserJournal/:sub",
  method: "get",
  handler: async (req, res) => {
    const sub = req.params.sub;
    try {
      const data = await getUserJournal(sub);
      res.status(200).json(data);
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
