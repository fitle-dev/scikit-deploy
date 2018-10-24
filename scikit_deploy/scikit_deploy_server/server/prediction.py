import numpy as np


def predict(model, input_data, config):
    sample = config.process_input(input_data)
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    return config.process_output(res)
