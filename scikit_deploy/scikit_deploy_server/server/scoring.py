import pickle
import json
import pkg_resources
import numpy as np
import os
from flask import Blueprint, request, jsonify
from server.prediction import predict
from server.config import config
from server.logging import get_logger
from collections import Iterable

LOGGER = get_logger(__name__)

LOGGER.info("Started server with config")
LOGGER.info(json.dumps(config))

model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))

app_blueprint = Blueprint('app', __name__)


ROUTE = f"{config.get('endpoint', '/score')}"


class APIError(Exception):
    def __init__(self, message):
        super(APIError, self).__init__(message)
        self.message = message


def make_sample(data):
    sample = []
    for v in config["inputs"]:
        p = data.get(v["name"])
        if p is None:
            if "default" in v:
                p = v["default"]
            else:
                message = f'Missing input in query string: {v["name"]}'
                LOGGER.error(message)
                raise APIError(message)
        try:
            sample.append(float(p))
        except ValueError:
            message = f"Input could not be coerced to float: {v} = {p}"
            LOGGER.error(message)
            raise APIError(message)
    return sample


@app_blueprint.route(ROUTE, methods=['GET'])
def score_endpoint():
    LOGGER.info("Received scoring request")
    try:
        sample = make_sample(request.args)
    except APIError as e:
        return e.message, 400
    prediction = predict(model, sample, config["outputs"])
    LOGGER.info("Successful prediction")
    return jsonify(dict(prediction=prediction))


@app_blueprint.route(f'{ROUTE}/multiple', methods=['POST'])
def score_multiple():
    LOGGER.info('Received scoring request for multiple samples')
    data = request.get_json()
    if not isinstance(data, Iterable):
        return "Body should be a json array of parameters", 400
    res = [dict(prediction=predict(model, make_sample(x), config["outputs"]))
           for x in data]
    return jsonify(res)


@app_blueprint.route("/instance/health", methods=['GET'])
def health():
    return "healthy", 200
