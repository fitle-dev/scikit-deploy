
import pickle
import numpy as np
import json
from server.scoring import predict
from server.config import Config
import os.path as osp


def validate_model(clf, endpoint):
    sample = {i['name']: 0.0 for i in endpoint.inputs}
    x = predict(clf, sample, endpoint)
    json.dumps(x)


if __name__ == "__main__":
    with open("./server/resources/config.json") as f:
        config = Config(json.load(f))
    for endpoint in config.endpoints:
        with open(osp.join("./server/resources", endpoint.model_name), 'rb') as f:
            clf = pickle.load(f)
            validate_model(clf, endpoint)
