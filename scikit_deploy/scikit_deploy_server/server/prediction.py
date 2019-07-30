import numpy as np

def predict(model, input_data, config):
    # sample = config.process_input(input_data)
    # vec = np.array(sample).reshape(1, -1)
    print(0, input_data)
    sample = {k: float(v) for k,v in dict(input_data).items()}
    print(1, sample)
    res = model.predict(sample, "raw")
    print(2, res)
    print(3, res.to_dict())
    # return config.process_output(res)
    return res.to_dict()

