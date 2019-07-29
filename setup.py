from setuptools import setup, find_packages
import re
import io

with open("README.md", "r") as f:
    long_descr = f.read()

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('scikit_deploy/__init__.py', encoding='utf_8_sig').read()
).group(1)

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
    version=__version__,
    description="Scikit-learn model REST API deployment with docker",
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author="Fitle",
    author_email="nerds@fitle.com",
    url="https://github.com/fitle-dev/scikit-deploy"
)
