import http from "http";
import https from "https";
import { URL } from "url";

function callRemoteService(
  call,
  catchExceptions,
  remoteTimeout,
  req,
  resolve,
  reject,
) {
  let headers = {
    "Content-Type": "application/json",
  };
  // removed logic to decide what happens w/ w/o agent
  headers = req.headers;
  const opts = {
    ...new URL(call),
    headers,
  };

  const h = opts.protocol === "https:" ? https : http;

  const r = h
    .get(opts, function (res, req) {
      const body = [];
      res.on("data", (chunk) => body.push(chunk));
      res.on("end", () => resolve(body.join("")));
    })
    .on("error", function (err) {
      if (catchExceptions) {
        resolve(err);
      } else {
        reject(err);
      }
    });
  r.setTimeout(remoteTimeout, function () {
    reject({ code: 500, message: "Read timed out" });
  });
}

export default callRemoteService;
