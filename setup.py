import re
from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="scikit-deploy",
    packages=["scikit_deploy"],
    install_requires=[
        'docker',
    ],
    entry_points={
        "console_scripts": ['skdeploy = scikit_deploy.main:main']
    },
    version="1.1",
    description="Scikit-learn model REST API deployment with docker",
    long_description=long_descr,
    author="Ulysse Mizrahi",
    author_email="ulysse.mizrahi@gmail.com",
    url="https://github.com/odusseys/scikit-deploy",
)
