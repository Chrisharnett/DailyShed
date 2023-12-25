import jwt from "jsonwebtoken";
// import { awsUserPool } from "../util/awsUserPool.js";
import bcrypt from "bcrypt";
import { db } from "../db.js";

// Temp import for basic setup. Remove bcrypt from dependencies when finished

export const signUpRoute = {
  path: "/api/signup",
  method: "post",
  handler: async (req, res) => {
    const { email, password } = req.body;

    const database = db;
    const user = await database.collection("users").findOne({ email });

    if (user) {
      return res.status(409).json({ message: "User already exists." });
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const startingInfo = {
      instrumet: "alto sax",
      birthdate: "15/03/1979",
    };

    const result = await database.collection("users").insertOne({
      email,
      passwordHash,
      info: startingInfo,
      isVerified: false,
    });

    const { insertedId } = result;

    console.log({
      id: insertedId,
      email,
      info: startingInfo,
      isVerified: false,
    });

    jwt.sign(
      {
        id: insertedId,
        email,
        info: startingInfo,
        isVerified: false,
      },
      process.env.JWT_SECRET,
      {
        expiresIn: "2d",
      },
      (err, token) => {
        if (err) {
          return res.status(500).send(err);
        }
        res.status(200).json({ token });
      }
    );
  },
};
