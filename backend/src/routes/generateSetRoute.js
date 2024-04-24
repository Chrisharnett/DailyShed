import axios from "axios";

export const generateSetRoute = {
  path: "/api/generateSet/:sub",
  method: "post",
  handler: async (req, res) => {
    const sub = req.params.sub;

    const playerDetails = req.body;

    const setGenerator = "http://127.0.0.1:5000/generateSet";

    try {
      const response = await axios.post(
        setGenerator,
        // { sub },
        playerDetails,
        {
          headers: { "Content-Type": "application/json" },
        }
      );

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
