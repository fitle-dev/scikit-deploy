import re
from setuptools import setup, find_packages

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="scikit-deploy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docker',
    ],
    entry_points={
        "console_scripts": ['skdeploy = scikit_deploy.main:main']
    },
    version="1.2",
    description="Scikit-learn model REST API deployment with docker",
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author="Fitle",
    author_email="nerds@fitle.com",
    url="https://github.com/fitle-dev/scikit-deploy"
)
