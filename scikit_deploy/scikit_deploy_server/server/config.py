import json
import pkg_resources
from typing import Dict

from server.logging import get_logger
from server.endpoint import Endpoint

LOGGER = get_logger(__name__)


class Config:
    def __init__(self, config_data:Dict=None):
        if not config_data:
            config_data = json.loads(pkg_resources.resource_string(
                __name__, 'resources/config.json'))
        self.config_data = config_data
        self.endpoints = []
        endpoints = config_data.get('endpoints')
        for endpoint_data in endpoints:
            self.endpoints.append(Endpoint(endpoint_data))
