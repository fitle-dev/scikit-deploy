import json
import pkg_resources
import numpy as np
from typing import Union
from server.logging import get_logger
from server.util import APIError, to_float

LOGGER = get_logger(__name__)


class Config:
    def __init__(self, config_data=None):
        if not config_data:
            config_data = json.loads(pkg_resources.resource_string(
                __name__, 'resources/config.json'))
        self._config = config_data
        self.route = f"{config_data.get('endpoint', '/score')}"
        self.inputs = config_data["inputs"]
        self.outputs = config_data["outputs"]

    def _normalize_input(self, value: Union[str, int, float], input_info: dict):
        try:
            return(
                float(value) - input_info.get('offset', 0)) / input_info.get('scaling', 1)
        except ValueError:
            message = f"Input could not be coerced to float: {input_info} = {value}"
            LOGGER.error(message)
            raise APIError(message)

    def _denormalize_output(self, value: Union[float, np.float], output_info: dict):
        return (to_float(value) * output_info.get('scaling', 1)) + output_info.get('offset', 0)

    def process_input(self, data):
        sample = []
        for input_info in self.inputs:
            value = data.get(input_info["name"])
            if value is None:
                if "default" in input_info:
                    value = input_info["default"]
                else:
                    message = f'Missing input in query string: {input_info["name"]}'
                    LOGGER.error(message)
                    raise APIError(message)
            sample.append(self._normalize_input(value, input_info))
        return sample

    def process_output(self, results):
        if len(self.outputs) == 1:
            return {self.outputs[0]['name']: self._denormalize_output(results, self.outputs[0])}
        return {b['name']: self._denormalize_output(a, b) for a, b in zip(results[0], self.outputs)}
