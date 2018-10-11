import tempfile
import shutil
import logging
import pkg_resources
import sys
import os.path as osp
import docker
import json


def prepare_workspace(temp_dir, clf_path, config_path):
    shutil.copytree(pkg_resources.resource_filename(
        __name__, "scikit_deploy_server"), osp.join(temp_dir, "workspace"))
    resources_folder = osp.join(temp_dir, "workspace", "server", "resources")
    shutil.copy(clf_path, osp.join(resources_folder, "clf.pkl"))
    shutil.copy(config_path, osp.join(resources_folder, "config.json"))


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
                rm=False
            )
        except docker.errors.BuildError as e:
            logging.error("Docker build failed with logs: ")
            for l in e.build_log:
                logging.error(l)
            raise


def validate_url_prefix(url_prefix: str):
    if len(url_prefix) == 0:
        return
    if not url_prefix.startswith("/"):
        logging.error("url_prefix must begin with a / or be empty.")
        raise ValueError()
    if url_prefix.endswith("/"):
        logging.error("url_prefix cannot end with a /")
        raise ValueError()


def build(clf_path, config_path):
    temp_dir = tempfile.mkdtemp()
    try:
        with open(config_path) as f:
            config = json.load(f)
        image_tag = config.get("image_tag")
        if image_tag is None:
            logging.error("No image_tag specified in config")
            exit(1)
        validate_url_prefix(config.get("url_prefix", ""))
        prepare_workspace(temp_dir, clf_path, config_path)
        build_docker(temp_dir, image_tag)
        logging.info("Successfully built image {}".format(image_tag))
        status = 0
    except:
        logging.error("Failed to build image")
        status = 1
    finally:
        shutil.rmtree(temp_dir)
        exit(status)
