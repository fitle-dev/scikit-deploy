import tempfile
import shutil
import logging
import pkg_resources
import sys
import os.path as osp
import docker
import json
import pickle

logger = logging.getLogger("scikit-deploy")


def _prepare_requirements(temp_dir, requirements_path):
    """
    Concatenates an user-provided requirements file with the default one.
    """
    # read default requirements
    final_path = osp.join(temp_dir, "workspace", "requirements.txt")
    with open(final_path) as f:
        reqs = f.read()
    # concatenate with user-specified
    with open(requirements_path) as f:
        reqs = "{}\n{}".format(reqs, f.read())
    # write back to file
    with open(final_path, "w+") as f:
        f.write(reqs)


def _prepare_workspace(temp_dir, clf_path, config_path, requirements_path):
    """
    Prepares the temporary workspace directory for the docker build
    """
    # copy the server package as the workspace directory
    shutil.copytree(pkg_resources.resource_filename(
        __name__, "scikit_deploy_server"), osp.join(temp_dir, "workspace"))

    # copy resources (clf, config) to the workspace server resources
    resources_folder = osp.join(temp_dir, "workspace", "server", "resources")
    shutil.copy(clf_path, osp.join(resources_folder, "clf.pkl"))
    shutil.copy(config_path, osp.join(resources_folder, "config.json"))
    if requirements_path is not None:
        _prepare_requirements(temp_dir, requirements_path)


def _build_docker(temp_dir, image_tag):
    path = osp.join(temp_dir, "workspace")
    client = docker.APIClient()
    try:
        output = client.build(
            path=path,
            dockerfile="Dockerfile",
            tag=image_tag,
            quiet=False,
            network_mode="host"
        )
        for l in output:
            logs = l.decode("utf-8").split("\r\n")
            for line in logs:
                if line:
                    line = json.loads(line)
                    if "stream" in line:
                        logger.info("(DOCKER) - {}".format(line["stream"]))
    except docker.errors.BuildError as e:
        logger.error("Docker build failed with logs: ")
        for l in e.build_log:
            logger.error(l)
        raise


def _validate_endpoint(endpoint: str):
    if not endpoint.startswith("/"):
        logger.error("endpoint must begin with a /")
        raise ValueError()
    if endpoint.endswith("/"):
        logger.error("endpoint cannot end with a /")
        raise ValueError()


def _generate_request(config):
    endpoint = config.get("endpoint", "/score")
    qs = "&".join([f"{o['name']}=0" for o in config["inputs"]])
    return f"http://localhost:8000{endpoint}?{qs}"


def build(clf_path, config_path, requirements_path):
    """
    Builds the docker image
    """
    logger.info("Beginning build.")
    temp_dir = tempfile.mkdtemp()
    try:
        with open(config_path) as f:
            config = json.load(f)
            image_tag = config.get("image_tag")
            if image_tag is None:
                logger.error("No image_tag specified in config")
                exit(1)
            if "endpoint" in config:
                _validate_endpoint(config["endpoint"])
            _prepare_workspace(temp_dir, clf_path,
                               config_path, requirements_path)
            _build_docker(temp_dir, image_tag)
            logger.info("Successfully built image {}".format(image_tag))
            logger.info("To test, run :")
            logger.info("   docker run -p 8000:8000 {}".format(image_tag))
            logger.info("and then perform http request")
            logger.info("   GET {}".format(_generate_request(config)))
            status = 0
    except:
        logger.exception("Failed to build image")
        status = 1
    finally:
        shutil.rmtree(temp_dir)
        exit(status)
