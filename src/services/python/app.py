import os
import json
import logging
import time
import random
from flask import Flask, request, jsonify
import requests
import importlib.util

# Load configuration from environment variables
config = json.loads(os.getenv("APP_CONFIG"))
log_dir = os.getenv("LOG_DIRECTORY", ".")
custom_code_dir = os.getenv("CUSTOM_CODE_DIR", ".")

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'python.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# Initialize Flask app
app = Flask(__name__)

# Set up Redis cache if needed (example uses local Redis)
#cache = redis.Redis(host='localhost', port=6379, db=0)
# Set port
port = int(os.environ.get('PORT', 8080))
endpoints = config.get('endpoints', {}).get('http', {})
print(f"Config: {config}")
print(f"Endpoints: {endpoints}")

def build_response(timeout):
    time.sleep(timeout)
    return f"{timeout} slow response"

def load_from_cache(timeout):
    time.sleep(timeout)  # Simulate delay#
    return f"{timeout} send data to cache"

def execute_custom_script(script, req):
    script_path = os.path.join(custom_code_dir, script)
    custom_script = importlib.util.module_from_spec(spec)
    spec = importlib.util.spec_from_file_location("custom_script", script_path)
    spec.loader.exec_module(custom_script)
    return custom_script.run(req)  # Assume custom script has a run method

def call_remote_service(call, req):
    try:
        if call.startswith("http://"):
            response = requests.get(call)
            return response.json()
        return None
    except Exception as e:
        logger.error("Error calling remote service: %s", e)
        return None

def process_call(call, req):
    if call.startswith("error"):
        _, code, message = call.split(",")
        raise Exception(f"Code: {code}, Message: {message}")
    elif call.startswith("sleep"):
        _, timeout = call.split(",")
        time.sleep(int(timeout))
        return f"Slept for {timeout}"
    elif call.startswith("slow"):
        _, timeout = call.split(",")
        return build_response(int(timeout))
    elif call.startswith("cache"):
        _, timeout = call.split(",")
        return load_from_cache(int(timeout))
    elif call.startswith("code"):
        _, script = call.split(",")
        return execute_custom_script(script, req)
    elif call.startswith("http://"):
        return call_remote_service(call, req)
    else:
        return f"{call} is not supported"

@app.route('/<path:endpoint>', methods=['GET', 'POST'])
def handle_request(endpoint):
    my_endpoint = "/" + endpoint
    logger.info(f"Endpoint: {my_endpoint}")
    if my_endpoint in endpoints:
        calls = endpoints[my_endpoint]
        logger.info(f"Endpoint: {my_endpoint}")
        results = []
        for call in calls:
            try:
                logger.info(f"Process call {call}")
                result = process_call(call, request)
                results.append(result)
            except Exception as e:
                logger.error(e)
                return jsonify({"error": str(e)}), 500
        return jsonify(results)
    else:
        return '404 Not Found', 404

@app.route("/")
def home():
    return "Home"

@app.route("/healthz", methods=['GET', 'POST'])
def health():
    return "OK"

if __name__ == "__main__":
    print(f"app-simulator running on port {port}")
    app.run(host='0.0.0.0', debug=False, port=port)