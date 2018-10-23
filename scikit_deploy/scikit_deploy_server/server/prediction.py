import numpy as np
from server.config import config


def predict(model, input_data):
    sample = config.process_input(input_data)
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    if len(config.outputs) == 1:
        return {config.outputs[0]: config.process_output(res[0])}
    return {a: config.process_output(b) for a, b in zip(config.outputs, res[0])}
