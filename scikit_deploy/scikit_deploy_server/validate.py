
import pickle
import numpy as np
import json
from server.scoring import predict


def validate_model(clf, config):
    sample = [0.0 for _ in config["inputs"]]
    x = predict(clf, sample, config["outputs"])
    json.dumps(x)


if __name__ == "__main__":
    with open("./server/resources/clf.pkl", 'rb') as f:
        clf = pickle.load(f)
    with open("./server/resources/config.json") as f:
        config = json.load(f)
    validate_model(clf, config)
