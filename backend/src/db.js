import { MongoClient } from "mongodb";
import "dotenv/config";

let db;

async function connectToDb(cb) {
  const client = new MongoClient(process.env.MONGO_CONNECT, {
    tls: true,
  });
  await client.connect();
  //set name of database
  db = client.db("TheShed");
  cb();
}

export { db, connectToDb };
