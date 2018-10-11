import tempfile
import shutil
import logging
import pkg_resources
import sys
import os.path as osp
import docker
import json
import pickle


def prepare_workspace(temp_dir, clf_path, config_path, requirements_path):
    shutil.copytree(pkg_resources.resource_filename(
        __name__, "scikit_deploy_server"), osp.join(temp_dir, "workspace"))
    resources_folder = osp.join(temp_dir, "workspace", "server", "resources")
    shutil.copy(clf_path, osp.join(resources_folder, "clf.pkl"))
    shutil.copy(config_path, osp.join(resources_folder, "config.json"))
    if requirements_path is not None:
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


def build_docker(temp_dir, image_tag):
    path = osp.join(temp_dir, "workspace")
    with open(osp.join(path, "Dockerfile"), 'rb') as dockerfile:
        client = docker.from_env()
        try:
            client.images.build(
                path=path,
                dockerfile="Dockerfile",
                tag=image_tag,
                quiet=False,
                rm=False,
                network_mode="host"
            )
        except docker.errors.BuildError as e:
            logging.error("Docker build failed with logs: ")
            for l in e.build_log:
                logging.error(l)
            raise


def _validate_url_prefix(url_prefix: str):
    if not url_prefix:
        return
    if not url_prefix.startswith("/"):
        logging.error("url_prefix must begin with a / or be empty.")
        raise ValueError()
    if url_prefix.endswith("/"):
        logging.error("url_prefix cannot end with a /")
        raise ValueError()


def build(clf_path, config_path, requirements_path):
    """
    Builds the docker image
    """
    temp_dir = tempfile.mkdtemp()
    try:
        with open(config_path) as f:
            config = json.load(f)
        image_tag = config.get("image_tag")
        if image_tag is None:
            logging.error("No image_tag specified in config")
            exit(1)
        _validate_url_prefix(config.get("url_prefix", ""))
        prepare_workspace(temp_dir, clf_path, config_path, requirements_path)
        build_docker(temp_dir, image_tag)
        logging.info("Successfully built image {}".format(image_tag))
        status = 0
    except:
        logging.exception("Failed to build image")
        status = 1
    finally:
        shutil.rmtree(temp_dir)
        exit(status)
