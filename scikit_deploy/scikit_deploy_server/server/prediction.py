from typing import Dict, Optional, Union

import numpy as np
from werkzeug import ImmutableMultiDict

from .endpoint import Endpoint


def predict(model, input_data:Union[Dict, ImmutableMultiDict], config:Endpoint):
    #new model
    if hasattr(model, "public_inputs"):
        sample = {k: float(v) for k,v in dict(input_data).items()}
        res = model.predict(sample, "raw")
        return res.to_dict("records")
    sample = config.process_input(input_data)
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    return config.process_output(res)
