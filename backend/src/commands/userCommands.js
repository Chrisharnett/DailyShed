import dotenv from "dotenv";
import AWS from "aws-sdk";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand } from "@aws-sdk/lib-dynamodb";

dotenv.config();

AWS.config.update({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const tableName = process.env.USERS_TABLE;

export const getUserData = async (sub) => {
  const command = new GetCommand({
    TableName: tableName,
    Key: {
      sub: sub,
    },
  });

  const response = await docClient.send(command);
  console.log(response);
  return response;
};

export const putUserData = async (user) => {
  const [sub, name, email, currentStatus, previousSet, exerciseHistory] = user;
  const command = new PutCommand({
    TableName: tableName,
    Item: {
      sub: sub,
      email: email,
      name: name,
      currentStatus: currentStatus,
      previousSet: previousSet,
      exerciseHistory: exerciseHistory,
    },
  });

  const response = await docClient.send(command);
  console.log(response);
  return response;
};
