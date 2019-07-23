import argparse
import logging
from scikit_deploy import __version__

from scikit_deploy.build import build


def _setup_logging():
    logger = logging.getLogger("scikit-deploy")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main(args_array=None):
    _setup_logging()
    parser = argparse.ArgumentParser(
        prog="skdeploy", description="Deploy scikit models as a REST API using Docker"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    parser.add_argument(
        "-c",
        dest="config_path",
        help="The path to the scikit-deploy config.json (see documentation).",
        nargs=1,
        required=True,
    )

    parser.add_argument(
        "-r",
        dest="requirements_path",
        help="Path for (optional) requirements.txt file to be used as dependencies of your model.",
        default=None,
        nargs=1,
    )

    parser.add_argument(
        "-k",
        dest="ssh_key",
        help="(optional) ssh key if your model dependencies uses private modules.",
        default=None,
        nargs=1,
    )
    args = parser.parse_args(args_array)
    requirements_path = args.requirements_path
    ssh_key = args.ssh_key[0] if hasattr(args, "ssh_key") and args.ssh_key is not None else None
    if requirements_path is not None:
        requirements_path = requirements_path[0]
    build(args.config_path[0], requirements_path, ssh_key)
