import tempfile
import shutil
import logging
import pkg_resources
import sys
import os.path as osp
import docker
import json
import pickle
from typing import Optional

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


def _prepare_workspace(temp_dir, config, requirements_path):
    """
    Prepares the temporary workspace directory for the docker build
    """
    # copy the server package as the workspace directory
    shutil.copytree(
        pkg_resources.resource_filename(__name__, "scikit_deploy_server"),
        osp.join(temp_dir, "workspace"),
    )

    # copy resources (clf, config) to the workspace server resources
    resources_folder = osp.join(temp_dir, "workspace", "server", "resources")
    json.dump(config, open(osp.join(resources_folder, "config.json"), "w"))
    for endpoint in config["endpoints"]:
        shutil.copy(
            endpoint["model_path"], osp.join(resources_folder, endpoint["model_name"])
        )
    if requirements_path is not None:
        _prepare_requirements(temp_dir, requirements_path)


def _build_docker(temp_dir, image_tag, ssh_key: Optional[str] = None):
    path = osp.join(temp_dir, "workspace")
    client = docker.APIClient()
    try:
        if ssh_key is None:
            output = client.build(
                path=path,
                dockerfile="Dockerfile",
                tag=image_tag,
                quiet=False,
                network_mode="host",
            )
        else:
            output = client.build(
                path=path,
                dockerfile="Dockerfile-multi-stage",
                tag=image_tag,
                quiet=False,
                network_mode="host",
                forcerm=True,  # ensure SSH keys don't persist
                target="multi-stage-build-final",
                buildargs=dict(SSH_PRIVATE_KEY=ssh_key),
            )
        for l in output:
            logs = l.decode("utf-8").split("\r\n")
            for line in logs:
                if line:
                    line = json.loads(line)
                    # Show only relevant outputs
                    if "stream" in line:
                        logger.info("(DOCKER) - {}".format(line["stream"]))
                    if "errorDetail" in line:
                        logger.error("(DOCKER) - {}".format(line["errorDetail"]))
    except (docker.errors.BuildError, docker.errors.APIError) as e:
        logger.error("Docker build failed with logs: ")
        for l in e.build_log:
            logger.error(l)
        raise


def _validate_route(route: str):
    if not route.startswith("/"):
        logger.error("route must begin with a /")
        raise ValueError()
    if route.endswith("/"):
        logger.error("route cannot end with a /")
        raise ValueError()


def _generate_request(config):
    endpoint = config["endpoints"][0]
    route = endpoint["route"]
    qs = "&".join([f"{o['name']}=0" for o in endpoint["inputs"]])
    return f"http://localhost:8000{route}?{qs}"


def build(config_path, requirements_path, ssh_key: Optional[str] = None):
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
            if "endpoints" not in config:
                logger.error("No endpoints specified in config")
                exit(1)
            for endpoint in config["endpoints"]:
                _validate_route(endpoint.get("route"))
                endpoint["model_name"] = (
                    endpoint["route"].replace("/", "_") + "_clf.pkl"
                )
            _prepare_workspace(temp_dir, config, requirements_path)
            _build_docker(temp_dir, image_tag, ssh_key)
            logger.info(f"Successfully built image {image_tag}")
            logger.info("To test, run :")
            logger.info(f"   docker run -p 8000:8000 {image_tag}")
            logger.info("and then perform http request")
            logger.info(f"   GET {_generate_request(config)}")
            status = 0
    except:
        logger.exception("Failed to build image")
        status = 1
    finally:
        shutil.rmtree(temp_dir)
        exit(status)
