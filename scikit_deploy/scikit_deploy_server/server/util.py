from typing import Union

import numpy as np


class APIError(Exception):
    def __init__(self, message, status_code):
        super(APIError, self).__init__(message)
        self.message = message
        self.status_code = status_code


def to_float(x:Union[float, np.float]):
    if type(x) == float:
        return x
    return x.item()  # numpy floats
