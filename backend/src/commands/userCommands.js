import dotenv from "dotenv";
import AWS from "aws-sdk";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  UpdateCommand,
  QueryCommand,
} from "@aws-sdk/lib-dynamodb";

dotenv.config();

AWS.config.update({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const user_table = process.env.USERS_TABLE;
const exercise_log_table = process.env.EXERCISE_LOG_TABLE;

export const getUserData = async (sub) => {
  const command = new GetCommand({
    TableName: user_table,
    Key: {
      sub: sub,
    },
  });
  const response = await docClient.send(command);
  return response;
};

export const getUserJournal = async (sub) => {
  const command = new QueryCommand({
    TableName: exercise_log_table,
    IndexName: "sub-index",
    KeyConditionExpression: "#sub = :subValue",
    ExpressionAttributeNames: {
      "#sub": "sub",
    },
    ExpressionAttributeValues: {
      ":subValue": sub,
    },
  });
  const response = await docClient.send(command);
  return response.Items;
};

export const putUserData = async (userData) => {
  const {
    sub,
    name,
    email,
    program,
    previousSet,
    exerciseHistory,
    exerciseMetadata,
  } = userData;
  const command = new PutCommand({
    TableName: user_table,
    Item: {
      sub: sub,
      email: email,
      name: name,
      program: program,
      previousSet: previousSet,
      exerciseHistory: exerciseHistory,
      exerciseMetadata: exerciseMetadata,
    },
  });
  const response = await docClient.send(command);
  return response;
};

// export const updatePreviousSet = async (playerDetails, previousSet) => {
//   const command = new UpdateCommand({
//     TableName: user_table,
//     Key: { sub: playerDetails.sub },
//     UpdateExpression: "set previousSet = :previousSet, program = :program",
//     ExpressionAttributeValues: {
//       ":previousSet": previousSet,
//       ":program": playerDetails.program,
//     },
//     ReturnValues: "ALL_NEW",
//   });

//   const response = await docClient.send(command);
//   const updatedPlayer = response.Attributes;

//   return updatedPlayer;
// };
