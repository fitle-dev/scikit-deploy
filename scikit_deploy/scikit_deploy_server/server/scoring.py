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
LOGGER.info(json.dumps(config._config))

model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))

app_blueprint = Blueprint('app', __name__)


@app_blueprint.route(config.route, methods=['GET'])
def score_endpoint():
    LOGGER.info("Received scoring request")
    try:
        prediction = predict(model, request.args, config)
    except APIError as e:
        return e.message, 400
    LOGGER.info("Successful prediction")
    return jsonify(dict(prediction=prediction))


@app_blueprint.route(config.route, methods=['POST'])
def score_multiple_endpoint():
    LOGGER.info('Received scoring request for multiple samples')
    data = request.get_json()
    if not isinstance(data, Iterable):
        return "Body should be a json array of parameters", 400
    try:
        res = [dict(prediction=predict(model, x, config))
               for x in data]
    except APIError as e:
        return e.message, 400
    return jsonify(res)


@app_blueprint.route("/instance/health", methods=['GET'])
def health():
    return "healthy", 200
