const { MongoClient } = require('mongodb');

async function main() {
    const uri= "mongodb+srv://saxDev:dRT0ZLfvGahCLmWf@cluster0.owezgre.mongodb.net/"

    const client = new MongoClient(uri);

    try {
        await client.connect();

        await listDatabases(client)

    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

main().catch(console.error);

async function listDatabases(client) {
    const databasesList = await client.db().admin().admin().listDatabases();
    console.log("Databases:");
    databasesList.databases.forEach(db => {
        console.log(`- ${db.name}`);
    })
}