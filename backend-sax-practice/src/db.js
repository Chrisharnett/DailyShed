import { MongoClient } from "mongodb";
import "dotenv/config";

let db;

async function connectToDb(cb) {
  const client = new MongoClient(process.env.MONGO_CONNECT, {
    tls: true,
    // local development
    // tlsCAFile: "devkeys/ca.pem",
    // tlsCertificateKeyFile: "devkeys/server-cert.pem",
    // deployment info
    // tlsCAFile: "/etc/letsencrypt/live/thesaxophoneshed.com/fullchain.pem",
    // tlsCertificateKeyFile: "/etc/letsencrypt/live/thesaxophoneshed.com/privkey.pem",
    // tlsAllowInvalidHostnames: false,
  });
  await client.connect();
  //set name of database
  db = client.db("TheShed");
  cb();
}

export { db, connectToDb };
