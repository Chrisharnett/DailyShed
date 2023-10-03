import { MongoClient } from "mongodb";

let db;
// Old uri connection. Maybe no atlas project attached.
// const uri = 'mongodb+srv://saxDev:dRT0ZLfvGahCLmWf@cluster0.owezgre.mongodb.net/'

// Atlas access
// let user = "dev";
// let pass = "mBqMsEyHkP2qxv9Z";
const uri = `mongodb+srv://${process.env.MONGO_USERNAME}:${process.env.MONGO_PASSWORD}@cluster0.2sjlgxi.mongodb.net/?retryWrites=true&w=majority`;

async function connectToDb(cb) {
  const client = new MongoClient(uri);
  await client.connect();
  //set name of database
  db = client.db("TheShed");
  cb();
}

export { db, connectToDb };
