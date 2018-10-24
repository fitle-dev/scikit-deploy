# scikit-deploy

Deploy models trained with scikit-learn with Docker.

## Requirements

You will need python 3 and Docker installed on your system.
You can deploy any model trained with scikit-learn, or which implements the same `predict()` method as scikit-learn models (eg. xgboost).

## Installing

There are two ways to install. First clone the repo.

### Install with setup.py

- Run `python setup.py install --force`

### Install with wheel

- Install the `wheel` package : `pip install wheel`
- Create a wheel : `pip wheel .`
- Install the wheel: `pip install scikit-deploy-{{SOME_VERSION_NUMBER}}.whl`

## Configuration

First, you will need a model trained using scikit-learn 0.20 (should support all versions later on) which has been pickled.

You will also need a `configuration.json` file describing the model metadata and build information.
It takes the following form:

```
{
    "image_tag": "{{the tag given to the generated docker image}}",
    "endpoint": "{{the endpoint to call for scoring. Defaults to 'score'}}",
    "cors": "{{boolean, whether to add CORS to the endpoint. Defaults to false.}}"
    "inputs": [{{the input features, objects with "name" and optional fields "default", "offset" and "scaling" }}],
    "outputs": [{{the output targets, objects with "name" and optional fields "offset" and "scaling"}}]
}
```

For inputs, the offset will be substracted to the value and then the difference will be divided by the scaling. For outputs, the offset will be added to the value and the sum will be multiplied by the scaling.
Offset and scaling values are typically used to normalize and denormalize the inputs and outputs respectively.

Here is an example config file :

```
{
    "image_tag": "my_super_model:latest",
    "endpoint": "/super-score",
    "inputs": [{"name": "x"}, {"name": "y", "default": 1.551, "offset": 50, "scaling": 2}],
    "outputs": [{"name": "z", "offset": 3, "scaling": 1.4}]
}
```

## Building your image

Run the following command:

`skdeploy -m /path/to/pickled/model -c /path/to/config.json`

This will run a Docker build using the image name you have provided.

If your model requires extra dependencies you can specify an additional `requirements.txt` file to include
for your server with the `-r`flag:

`skdeploy -m /path/to/model -c /path/to/config -r /path/to/requirements.txt`

## Running and testing the server

The server running inside the Docker container listens on port 5000.
To test your server on local port 8080 for example, run it using docker:

`docker run -p 8080:5000 your_image_tag`

And you can start querying the server ; for the config file above, this would be done as :

`GET localhost:8080/super-score?x=1337&y=115.16`

Which would yield the json

```
{
    "prediction": {
        "z": 11525
    }
}
```

You can also send a `POST` request to the endpoint. In this case, the body must be a JSON array of the inputs. Using the `POST` method, you can ask the server for several predictions in one request. For example:

```
[
    {"x": 1337, "y": 115.16},
    {"x": 2664, "y": 98.3},
]
```

Which would yield

```
{
    "prediction": [
        {"z": 11525},
        {"z": 3457}
    ]
}
```
