import json
import pkg_resources

config = json.loads(pkg_resources.resource_string(
    __name__, 'resources/config.json'))
