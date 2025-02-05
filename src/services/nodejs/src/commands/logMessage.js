function logMessage(logger, level, message) {
  if (logger.hasOwnProperty(level)) {
    logger[level](message);
  } else {
    logger.info(message);
  }
  return "Logged (" + level + "): " + message;
}

export default logMessage;
