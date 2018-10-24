class APIError(Exception):
    def __init__(self, message):
        super(APIError, self).__init__(message)
        self.message = message


def to_float(x):
    if type(x) == float:
        return x
    return x.item()  # numpy floats
