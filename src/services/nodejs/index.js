import process from "process";
import logger from "./src/logger.js";
import { startServer } from "./src/app.js";

const config = JSON.parse(process.env.APP_CONFIG);
const customCodeDir = process.env.CUSTOM_CODE_DIR;

let port = parseInt(process.argv[2]);
if (isNaN(port)) {
  port = 8080;
}

startServer(config, logger, customCodeDir, port);
