import axios from "axios";

export const flaskTestRoute = {
  path: "/api/flaskTest/",
  method: "get",
  handler: async (req, res) => {
    const exerciseMaker = "http://127.0.0.1:5000/";

    try {
      const response = await axios.get("http://127.0.0.1:5000/");

      if (response.status === 200) {
        console.log(response.data);
        res.status(200).json(response.data);
      } else {
        res.status(500).json({ error: "Error returned from server" });
      }
    } catch (error) {
      res.status(500).json({ error: "Error communicating with Flask server" });
    }
  },
};
