import numpy as np


def _float(x):
    if type(x) == float:
        return x
    return x.item()  # numpy floats


def predict(model, sample, outputs):
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    if len(outputs) == 1:
        return {outputs[0]: _float(res[0])}
    return {a: _float(b) for a, b in zip(outputs, res[0])}
