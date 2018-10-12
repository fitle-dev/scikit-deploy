import pickle
import json
import pkg_resources
import numpy as np
import os
from flask import Blueprint, request, jsonify
from server.prediction import predict
from server.config import config


model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))

app_blueprint = Blueprint('app', __name__)


ROUTE = f"{config.get('endpoint', '/score')}"


@app_blueprint.route(ROUTE, methods=['GET'])
def score_endpoint():
    sample = []
    for v in config["inputs"]:
        p = request.args.get(v["name"])
        if p is None:
            if "default" in v:
                p = v["default"]
            else:
                return f'Missing input in query string: {v["name"]}', 400
        try:
            sample.append(float(p))
        except ValueError:
            return f"Input could not be coerced to float: {v} = {p}", 400
    prediction = predict(model, sample, config["outputs"])
    return jsonify(dict(prediction=prediction))


@app_blueprint.route("/instance/health", methods=['GET'])
def health():
    return "healthy", 200
