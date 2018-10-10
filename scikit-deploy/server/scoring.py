import pickle
import json
import pkg_resources
import numpy as np

from flask import Blueprint, request, jsonify

model = pickle.loads(pkg_resources.resource_string(
    __name__, 'resources/clf.pkl'))
config = json.loads(pkg_resources.resource_string(
    __name__, 'resources/config.json'))

app_blueprint = Blueprint('app', __name__)


def _predict(sample):
    vec = np.array(sample).reshape(1, -1)
    return


@app_blueprint.route('/score', methods=['GET'])
def score_endpoint():
    sample = []
    for v in config['variables']:
        p = request.args.get(v)
        if p is None:
            return f'Missing variable in query string: {v}', 400
        sample.append(float(p))
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec).tolist()
    return jsonify(dict(prediction=res))
