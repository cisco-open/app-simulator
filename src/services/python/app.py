import os
import json
import time
import logging
import random
import requests
from flask import Flask, request, jsonify, Response
from cachetools import TTLCache
from datetime import datetime
from cronchecker import is_time_matching_cron
import pymysql
import urllib.parse

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)

# In-Memory Cache (TTL of 60 seconds, max size 100)
cache = TTLCache(maxsize=100, ttl=60)

# Load Config from Environment
env_app_config = os.getenv("APP_CONFIG", '{"endpoints": {"http": {}}}')
config = json.loads(env_app_config)
endpoints = config.get("endpoints", {}).get("http", {})

print(f"Loaded Endpoints: {endpoints}")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET"])
def handle_request(path):
    """Handles incoming requests based on configured endpoints."""
    endpoint = f"/{path}"
    logger.info(f"Endpoint requested: {endpoint}")

    if endpoint in endpoints:
        return process_endpoint(endpoints[endpoint])
    
    return Response("404 Not Found", status=404)

def is_scheduled(schedule):
    """Check if the current time matches the given cron schedule."""
    now = datetime.now()
    print(f"Time: {now}")
    print(f"Schedule {schedule}")
    return is_time_matching_cron(schedule, now)

def process_endpoint(endpoint_data):
    """Processes the configured endpoint JSON array."""
    result = []
    for entry in endpoint_data:
        response = pre_process_call(entry)
        result.append(str(response))
    return Response("\n".join(result), status=200)

def pre_process_call(call):
    """Processes individual call configurations."""
    if isinstance(call, list):
        call = random.choice(call)

    if isinstance(call, dict):
        probability = call.get("probability", 1.0)
        if random.random() > probability:
            print(f"probability hit")
            return f"{call.get('call')} was not probable"
        if "schedule" in call:
            print(f"scheduler hit")
            if not is_scheduled(call["schedule"]):
                print(f"scheduler active")
                return f"{call['call']} was not scheduled"
            else:
                print(f"was scheduled")
                return "was scheduled"

        return process_call(call.get("call"), call.get("catchExceptions", True), call.get("remoteTimeout", 1000))

    return process_call(call, True, 1000)

def process_call(call, catch_exceptions, remote_timeout):
    """Executes various actions based on call type."""
    logger.info(f"Processing call: {call}")

    try:
        if call.startswith("sleep"):
            timeout = int(call.split(",")[1].strip())
            time.sleep(timeout / 1000)
            return f"Slept for {timeout}ms"

        elif call.startswith("log"):
            parts = call.split(",")
            level = parts[1] if len(parts) > 2 else "info"
            message = parts[-1]
            log_message(level, message)
            return f"Logged ({level}): {message}"

        elif call.startswith("slow"):
            timeout = int(call.split(",")[1])
            return build_response(timeout)

        elif call.startswith("cache"):
            timeout = int(call.split(",")[1])
            return load_from_cache(timeout)

        elif call.startswith("http://") or call.startswith("https://"):
            return call_remote(call, catch_exceptions, remote_timeout)

        elif call.startswith("sql://"):
            return query_database(call, catch_exceptions, remote_timeout)

        elif call.startswith("error"):   
            return Response("500 Internal Server Error", status=500)

        elif call.startswith("image"):
            src = call.split(",")[1]
            return f"<img src='{src}' />"

        elif call.startswith("script"):
            src = call.split(",")[1]
            return f"<script src='{src}?output=javascript'></script>"

        elif call.startswith("ajax"):
            src = call.split(",")[1]
            return f"<script>var xhr = new XMLHttpRequest();xhr.open('GET', '{src}');xhr.send();</script>"

        return f":{call} is not supported"

    except Exception as e:
        if catch_exceptions:
            print(f"Caught exception in process_call")
            return f"Exception: {str(e)}"
        raise e

def log_message(level, message):
    """Logs messages at various levels."""
    level = level.lower()
    if level == "warn":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    elif level == "trace":
        logger.debug(message)  # Python doesn't have a "trace" level
    else:
        logger.info(message)

def build_response(timeout):
    """Simulates a slow response."""
    time.sleep(timeout / 1000)
    return f"{timeout}ms slow response"

def load_from_cache(timeout):
    """Simulates reading/writing to cache."""
    start = time.time()
    key = int(time.time() * 1000) % 1000  # Mock key
    cache[key] = key
    while (time.time() - start) < (timeout / 1000):
        pass
    return f"Cache result: {cache.get(key, 'Not found')}"

def query_database(call, catch_exceptions, remote_timeout):
    """Simulates executing an SQL query."""
    
    # Parse the call string to extract host, database name, and query
    parsed_url = urllib.parse.urlparse(call)
    # Extract the scheme (e.g., "sql"), host, and path (database name)
    host = parsed_url.hostname
    database_name = parsed_url.path.strip('/')
    query = urllib.parse.parse_qs(parsed_url.query)['query'][0]
    print(f"Connecting to {call}")
    print(f"Host:{host}, DB:{database_name}, query:{query}")
    # Establish a database connection using the parsed host and database name
    connection = pymysql.connect(
        host=host,  # dynamically set the host from the parsed URL
        user='root',
        password='root',
        database=database_name,
        connect_timeout=remote_timeout
        )
    try:
        # Prepare and execute the SQL statement
        with connection.cursor() as cursor:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                # Fetch all results if it's a SELECT query
                results = cursor.fetchall()
                return results
            else:
                # For INSERT, UPDATE, DELETE, etc., commit the transaction
                connection.commit()
                return f"Query executed successfully: {query}"

        # Commit changes for queries that modify the database
        connection.commit()

    except MySQLError as e:
        if catch_exceptions:
            return str(e)
        raise IOError(e)

    finally:
        if connection:
            connection.close()

    return f"Database query executed: {call}"


def call_remote(call, catch_exceptions, remote_timeout):
    """Performs an HTTP request."""
    try:
        response = requests.get(call, timeout=remote_timeout)
        return response.text
    except requests.RequestException as e:
        if catch_exceptions:
            return f"HTTP Error: {str(e)}"
        raise e

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)