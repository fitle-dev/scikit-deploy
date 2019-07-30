import pickle
import json
import pkg_resources
import numpy as np
import os
from flask import Blueprint, request, jsonify
from server.prediction import predict
from server.config import Config
from server.logging import get_logger
from server.util import APIError
from collections import Iterable

LOGGER = get_logger(__name__)

config = Config()

LOGGER.info("Started server with config")
LOGGER.info(json.dumps(config.config_data))

models = {}
endpoints_config = {}
for endpoint in config.endpoints:
    # We remove the leading /
    route_key = endpoint.route[1:]
    models[route_key] = pickle.loads(pkg_resources.resource_string(
        __name__, f'resources/{endpoint.model_name}'))
    endpoints_config[route_key] = endpoint

app_blueprint = Blueprint('app', __name__)


@app_blueprint.route('/<route>', methods=['GET'])
def index_endpoint(route:str):
    try:
        model = models.get(route)
        endpoint_config = endpoints_config.get(route)
        if not model:
            raise APIError('Not found', 404)
        LOGGER.info("Received scoring request")
        prediction = predict(model, request.args, endpoint_config)
    except APIError as e:
        return e.message, e.status_code
    LOGGER.info("Successful prediction")
    return jsonify(dict(prediction=prediction))


@app_blueprint.route('/<route>', methods=['POST'])
def score_multiple_endpoint(route:str):
    try:
        model = models.get(route)
        endpoint_config = endpoints_config.get(route)
        if not model:
            raise APIError('Not found', 404)
        LOGGER.info('Received scoring request for multiple samples')
        data = request.get_json()
        if not isinstance(data, Iterable):
            return "Body should be a json array of parameters", 400
        res = [dict(prediction=predict(model, x, endpoint_config))
               for x in data]
    except APIError as e:
        return e.message, e.status_code
    return jsonify(res)


@app_blueprint.route("/instance/health", methods=['GET'])
def health():
    return "healthy", 200


@app_blueprint.route("/config", methods=['GET'])
def config_endpoint():
    return jsonify(config.config_data), 200
