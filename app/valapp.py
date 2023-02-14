from datetime import time
import logging
import sys
import os
import json_logging
import redis

from flask import Flask

redis_host = os.environ['REDIS_HOST'] or 'redis'
redis_port = os.environ['REDIS_PORT'] or 6379
cache = redis.Redis(host=redis_host, port=redis_port)

app = Flask(__name__)

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("valogger")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def get_correl():
    return json_logging.get_correlation_id()

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    correlation_id = json_logging.get_correlation_id()
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)

@app.route('/ping')
def ping():
    return 'pong\n'

@app.route('/correl')
def correl():
    correl_id = get_correl()
    return 'json logger correlation id: {}\n'.format(correl_id)

@app.route('/forcerr')
def forcerr():
    correl_id = get_correl()
    return 'json logger forced error\n'
