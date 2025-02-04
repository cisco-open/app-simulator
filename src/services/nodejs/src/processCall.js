import cronmatch from "cronmatch";

import logMessage from "./commands/logMessage.js";
import buildResponse from "./commands/buildResponse.js";
import callRemoteService from "./commands/callRemoteService.js";
import { exec } from "child_process";

const commands = {
  error: ([code, message], _, reject) => {
    reject({ code, message });
  },
  sleep: ([timeout], resolve, _) => {
    setTimeout(function () {
      resolve(`Slept for ${timeout}`);
    }, timeout);
  },
  slow: ([timeout], resolve, _) => {
    resolve(buildResponse(timeout));
  },
  image: ([src], resolve, _) => {
    resolve(`<img src='${src}' />`);
  },
  script: ([src], resolve, _) => {
    resolve(`<script src='${src}?output=javascript'></script>`);
  },
  ajax: ([src], resolve, _) => {
    resolve(
      `<script>var o = new XMLHttpRequest();o.open('GET', '${src}');o.send();</script>`,
    );
  },
  log: (args, resolve, _, logger) => {
    if (args.length > 1) {
      console.log(args[0], args[1], args.length);
      resolve(logMessage(logger, args[0], args[1]));
    } else {
      resolve(logMessage(logger, "info", args[0]));
    }
  },
};

function preprocessCall(call) {
  const result = {
    call: call,
    remoteTimeout: 1073741824,
    catchExceptions: true,
    skip: false,
    skipReason: "",
  };

  // If call is an array, select one element as call
  if (Array.isArray(call)) {
    result.call = call[Math.floor(Math.random() * call.length)];
  }
  // If call is an object, check for probability
  if (typeof call === "object") {
    if (
      call.hasOwnProperty("probability") &&
      call.probability <= Math.random()
    ) {
      result.skipReason = `${call.call} was not probable`;
      result.skip = true;
    } else if (
      call.hasOwnProperty("schedule") &&
      !cronmatch.match(call.schedule, new Date())
    ) {
      result.skipReason = `${call.call} was not scheduled`;
      result.skip = true;
    }

    if (call.hasOwnProperty("remoteTimeout")) {
      result.remoteTimeout = call.remoteTimeout;
    }
    if (call.hasOwnProperty("catchExceptions")) {
      result.catchExceptions = call.catchExceptions;
    }
    return result;
  }

  return result;
}

function processCall(unprocessedCall, req, logger, customCodeDir) {
  return new Promise(function (resolve, reject) {
    logger.debug(unprocessedCall);
    const { call, remoteTimeout, catchExceptions, skipReason, skip } =
      preprocessCall(unprocessedCall);
    if (skip) {
      resolve(skipReason);
    } else {
      if (call.startsWith("http://") || call.startsWith("https://")) {
        callRemoteService(
          call,
          catchExceptions,
          remoteTimeout,
          req,
          resolve,
          reject,
        );
      } else {
        const [cmd, ...args] = call.split(",");
        if (commands.hasOwnProperty(cmd)) {
          commands[cmd](args, resolve, reject, logger);
        } else if (cmd === "code") {
          const [scripts] = args;
          executeCustomScript(customCodeDir, script, req, resolve, reject);
        } else {
          resolve(`${cmd} is not supported`);
        }
      }
    }
  });
}

export default processCall;
