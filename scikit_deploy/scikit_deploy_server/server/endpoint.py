from typing import Union, Dict, List
from server.util import APIError, to_float
from server.logging import get_logger
import numpy as np

LOGGER = get_logger(__name__)


class Endpoint:
    def __init__(self, endpoint_data:Dict):
        self.route = endpoint_data["route"]
        self.model_name = endpoint_data["model_name"]
        self.inputs = endpoint_data["inputs"]
        self.outputs = endpoint_data["outputs"]

    def _normalize_input(self, value: Union[str, int, float], input_info: Dict):
        try:
            return (float(value) - input_info.get("offset", 0)) / input_info.get(
                "scaling", 1
            )
        except ValueError:
            message = f"Input could not be coerced to float: {input_info} = {value}"
            LOGGER.error(message)
            raise APIError(message, 400)

    def _denormalize_output(self, value: Union[float, np.float], output_info: Dict):
        return (to_float(value) * output_info.get("scaling", 1)) + output_info.get(
            "offset", 0
        )

    def process_input(self, data:Dict) -> List[float]:
        sample = []
        for input_info in self.inputs:
            value = data.get(input_info["name"])
            if value is not None:
                sample.append(self._normalize_input(value, input_info))
            else:
                sample.append(0.0)
        return sample

    def process_output(self, results:List[List[Union[float, np.float]]]) -> Dict[str,Union[float, np.float]]:
        if len(self.outputs) == 1:
            return {
                self.outputs[0]["name"]: self._denormalize_output(
                    results, self.outputs[0]
                )
            }
        return {
            b["name"]: self._denormalize_output(a, b)
            for a, b in zip(results[0], self.outputs)
        }
