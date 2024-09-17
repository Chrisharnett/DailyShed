import express from "express";
import "dotenv/config.js";
import path from "path";
import { spawn } from "child_process";
import { routes } from "./routes/index.js";

import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 8000;

app.use(express.json());

// TODO: Is this approach acceptable for production??
app.use(express.static(path.join(__dirname, "../build")));

const venvPath = "./python_scripts/exGenerator";

const pythonExecutable = path.join(venvPath, "bin/python");

const flaskServerScriptPath = path.join(
  __dirname,
  "../python_scripts/exerciseMaker.py"
);

const flaskExerciseMaker = spawn(pythonExecutable, [flaskServerScriptPath]);

flaskExerciseMaker.stdout.on("data", (data) => {
  console.log(`Flask Server Output: ${data}`);
});

flaskExerciseMaker.stderr.on("data", (data) => {
  console.error(`Flask Server Error: ${data}`);
});

flaskExerciseMaker.on("close", (code) => {
  console.log(`Flask Server exited with code ${code}`);
});

routes.forEach((route) => {
  app[route.method](route.path, route.handler);
});

app.listen(port, () => {
  console.log("Server is listening on port 8000");
});
