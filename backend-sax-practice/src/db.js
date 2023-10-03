import { MongoClient } from "mongodb";
import "dotenv/config";

let db;

const uri = `mongodb+srv://${process.env.MONGO_USERNAME}:${process.env.MONGO_PASSWORD}@cluster0.2sjlgxi.mongodb.net/?retryWrites=true&w=majority`;

async function connectToDb(cb) {
  const client = new MongoClient(uri);
  await client.connect();
  //set name of database
  db = client.db("TheShed");
  cb();
}

export { db, connectToDb };
