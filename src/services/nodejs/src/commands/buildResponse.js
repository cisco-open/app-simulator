function buildResponse(timeout) {
  const start = process.hrtime();
  let elapsed = process.hrtime(start);
  let response = "";
  while (elapsed[0] * 1000000000 + elapsed[1] < timeout * 1000000) {
    response += " ";
    elapsed = process.hrtime(start);
  }
  return response.length + " slow response";
}

export default buildResponse;
