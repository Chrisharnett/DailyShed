import dotenv from "dotenv";
import AWS from "aws-sdk";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";

dotenv.config();

AWS.config.update({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const exercise_log_table = process.env.EXERCISE_LOG_TABLE;

export const logExercise = async (exerciseEntry) => {
  const { timestamp, sub, exercise, rating, comment, sessionID, exerciseName } =
    exerciseEntry;
  const command = new PutCommand({
    TableName: exercise_log_table,
    Item: {
      exerciseName: exerciseName,
      sessionID: sessionID,
      timestamp: timestamp,
      sub: sub,
      exercise: exercise,
      rating: rating,
      comment: comment,
    },
  });
  const response = await docClient.send(command);
  return response;
};
