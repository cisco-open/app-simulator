import log4js from "log4js";

export const logDir = process.env.LOG_DIRECTORY
  ? process.env.LOG_DIRECTORY
  : ".";

log4js.configure({
  appenders: {
    FILE: {
      type: "file",
      filename: `${logDir}/node.log`,
      layout: {
        type: "pattern",
        pattern: "%d{yyyy-MM-dd hh:mm:ss,SSS} [%z] %p %c - %m",
      },
    },
    CONSOLE: {
      type: "stdout",
      layout: {
        type: "pattern",
        pattern: "%d{yyyy-MM-dd hh:mm:ss,SSS} [%z] %p %c - %m",
      },
    },
  },
  categories: { default: { appenders: ["CONSOLE", "FILE"], level: "info" } },
});

var logger = log4js.getLogger();
logger.level = "debug";

export default logger;
