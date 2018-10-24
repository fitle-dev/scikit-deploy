
import pickle
import numpy as np
import json
from server.scoring import predict
from server.config import Config


def validate_model(clf, config):
    sample = {i['name']: 0.0 for i in config.inputs}
    x = predict(clf, sample, config)
    json.dumps(x)


if __name__ == "__main__":
    with open("./server/resources/clf.pkl", 'rb') as f:
        clf = pickle.load(f)
    with open("./server/resources/config.json") as f:
        config = Config(json.load(f))
    validate_model(clf, config)
