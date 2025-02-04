import { msleep } from "../sleep.js";
import path from "path";
import Chance from "chance";

const chance = new Chance();

function executeCustomScript(customCodeDir, script, req, resolve, reject) {
  var r = require(path.join(customCodeDir, script))({
    logger: logger,
    req: req,
    cronmatch: cronmatch,
    sleep: msleep,
    chance: chance,
  });
  if (r === false) {
    reject(`Script ${script} was not executed successfully`);
  } else if (
    typeof r === "object" &&
    r.hasOwnProperty("code") &&
    r.hasOwnProperty("code")
  ) {
    reject({ code: r.code, message: r.message });
  } else if (typeof r === "string") {
    resolve(r);
  } else {
    resolve(`Script ${script} was executed successfully`);
  }
}

export default executeCustomScript;
