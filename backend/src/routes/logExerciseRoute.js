import { logExercise } from "../commands/exercises.js";

export const logExerciseRoute = {
  path: "/api/logExercise",
  method: "post",
  handler: async (req, res) => {
    const exerciseEntry = req.body;

    try {
      const response = await logExercise(exerciseEntry);
      res.status(200).json({ response });
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  },
};
