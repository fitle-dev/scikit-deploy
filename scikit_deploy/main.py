import argparse
import logging 

from scikit_deploy.build import build

def _setup_logging():
    logger = logging.getLogger('scikit-deploy')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
def main():
    _setup_logging()
    parser = argparse.ArgumentParser(
        description="Deploy scikit models as a REST API using Docker")
    parser.add_argument('clf_path',
                        help="The path to your pickled scikit model.")
    parser.add_argument('config_path',
                        help="The path to the scikit-deploy config.json (see documentation).")

    parser.add_argument(
        '-r',
        dest="requirements_path",
        help="Path for (optional) requirements.txt file to be used as dependencies of your model.",
        default=None,
        nargs=1,
    )

    args = parser.parse_args()
    build(args.clf_path, args.config_path, args.requirements_path[0])
