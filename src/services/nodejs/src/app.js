import express from "express";
import bodyParser from "body-parser";
import url from "url";
import { msleep } from "./sleep.js";
import processCall from "./processCall.js";

function createApp(config, logger, customCodeDir) {
  const endpoints = config.endpoints.http;

  Object.keys(endpoints).forEach(function (key) {
    if (!key.startsWith("/")) {
      endpoints["/" + key] = endpoints[key];
      delete endpoints[key];
    }
  });

  const app = express();

  app.use(bodyParser.json()); // for parsing application/json
  app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

  app.use((req, res, next) => {
    const start = process.hrtime();
    res.on("finish", () => {
      const duration = process.hrtime(start);
      const responseTime = duration[0] * 1000 + duration[1] / 1e6;
      const logMessage = `${req.ip} - "${req.method} ${req.originalUrl} HTTP/${req.httpVersion}" ${res.statusCode} ${res.get("Content-Length") || 0} "${req.headers["user-agent"]}" - ${responseTime.toFixed(3)} ms`;
      logger.debug(logMessage);
    });
    next();
  });

  async function processRequest(req, res, params) {
    const path = new URL(req.url, `http://${req.headers.host}`).pathname;
    logger.info("Request Headers:", req.headers);
    if (endpoints.hasOwnProperty(path)) {
      try {
        const results = [];
        for (let i = 0; i < endpoints[path].length; i++) {
          const call = endpoints[path][i];
          results.push(await processCall(call, req, logger, customCodeDir));
        }
        if (req.query.output && req.query.output === "javascript") {
          res.send(results);
        } else {
          res.send(results);
        }
      } catch (reason) {
        logger.error(reason);
        res
          .status(typeof reason.code === "number" ? reason.code : 500)
          .send(reason.message);
      }
    } else {
      res.status(404).send("404");
    }
  }

  app.get("/**", function (req, res) {
    processRequest(req, res, req.query);
  });

  app.post("/**", function (req, res) {
    processRequest(req, res, req.body);
  });

  return app;
}

function startServer(config, logger, customCodeDir, port = 8080) {
  const app = createApp(config, logger, customCodeDir);

  const server = app.listen(port, () =>
    logger.info(
      `Running ${config.name} (type: ${config.type}) on port ${port}`,
    ),
  );
  logger.debug(`Configuration:`);
  logger.debug(JSON.stringify(config));

  if (config.hasOwnProperty("options")) {
    server.on("connection", (socket) => {
      if (config.options.hasOwnProperty("connectionDelay")) {
        msleep(config.options.connectionDelay);
      }
      if (
        config.options.hasOwnProperty("lossRate") &&
        parseFloat(config.options.lossRate) >= Math.random()
      ) {
        socket.end();
        throw new Error("An error occurred");
      }
    });
  }
}

export { createApp, startServer };
