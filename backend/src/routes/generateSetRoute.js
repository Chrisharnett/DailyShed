import axios from "axios";

export const generateSetRoute = {
  path: "/api/generateSet/",
  method: "post",
  handler: async (req, res) => {
    const user = req.body;
    // valid data: console.log(req.body);

    const exerciseMaker = "http://127.0.0.1:5000/getSet";

    try {
      const response = await axios.post(exerciseMaker, user, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.status === 200) {
        res.status(200).json(response.data);
      } else {
        res.status(500).json({ error: "Image generation failed" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
