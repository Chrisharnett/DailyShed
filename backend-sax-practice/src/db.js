import { MongoClient } from 'mongodb'

let db;
const uri = 'mongodb+srv://saxDev:dRT0ZLfvGahCLmWf@cluster0.owezgre.mongodb.net/'

async function connectToDb(cb) {
    const client = new MongoClient(uri)
    await client.connect();
    //set name of database
    db = client.db('TheShed');
    cb()
}

export {
    db,
    connectToDb
};