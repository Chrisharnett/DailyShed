import dotenv from "dotenv";
import AWS from "aws-sdk";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
} from "@aws-sdk/lib-dynamodb";

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
  return response;
};

export const putUserData = async (userData) => {
  const { sub, name, email, program, previousSet, exerciseHistory } = userData;
  const command = new PutCommand({
    TableName: tableName,
    Item: {
      sub: sub,
      email: email,
      name: name,
      program: program,
      previousSet: previousSet,
      exerciseHistory: exerciseHistory,
    },
  });
  const response = await docClient.send(command);
  return response;
};
