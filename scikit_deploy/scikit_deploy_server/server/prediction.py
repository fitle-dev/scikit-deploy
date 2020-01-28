from typing import Dict, Optional, Union

import numpy as np
from werkzeug import ImmutableMultiDict

from .endpoint import Endpoint


def predict(model, input_data: Union[Dict, ImmutableMultiDict], config: Endpoint):
    # new model
    if hasattr(model, "public_inputs"):
        sample = {}
        for k, v in dict(input_data).items():
            try:
                # GET request arguments are strings. If they should in fact be number, we try to convert them here
                sample[k] = float(v)
            except ValueError:
                # Some arguments are in fact strings. So we let them.
                sample[k] = v
        res = model.predict(sample, "raw")
        return res.to_dict("records")[0]
    sample = config.process_input(input_data)
    vec = np.array(sample).reshape(1, -1)
    res = model.predict(vec)
    return config.process_output(res)
