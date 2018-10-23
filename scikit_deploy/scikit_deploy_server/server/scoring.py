import pickle
import json
import pkg_resources
import numpy as np
import os
from flask import Blueprint, request, jsonify
from server.prediction import predict
from server.config import config
from server.logging import get_logger
from server.util import APIError
from collections import Iterable

LOGGER = get_logger(__name__)

LOGGER.info("Started server with config")
LOGGER.info(json.dumps(config))

model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))

app_blueprint = Blueprint('app', __name__)


@app_blueprint.route(config.route, methods=['GET'])
def score_endpoint():
    LOGGER.info("Received scoring request")
    try:
        sample = config.process_input(request.args)
    except APIError as e:
        return e.message, 400
    prediction = predict(model, sample, config)
    LOGGER.info("Successful prediction")
    return jsonify(dict(prediction=prediction))


@app_blueprint.route(config.route, methods=['POST'])
def score_multiple_endpoint():
    LOGGER.info('Received scoring request for multiple samples')
    data = request.get_json()
    if not isinstance(data, Iterable):
        return "Body should be a json array of parameters", 400
    res = [dict(prediction=predict(model, config.process_input(x), config))
           for x in data]
    return jsonify(res)


@app_blueprint.route("/instance/health", methods=['GET'])
def health():
    return "healthy", 200
