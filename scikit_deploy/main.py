import argparse
from scikit_deploy.build import build


def main():
    parser = argparse.ArgumentParser(
        description="Deploy scikit models as a REST API using Docker")
    parser.add_argument('clf_path',
                        help="The path to your pickled scikit model.")
    parser.add_argument('config_path',
                        help="The path to the scikit-deploy config.json (see documentation).")

    args = parser.parse_args()
    build(args.clf_path, args.config_path)
