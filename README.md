# scikit-deploy

Deploy models trained with scikit-learn with Docker.

## Requirements

You will need python 3 and Docker installed on your system.
You can deploy any model trained with scikit-learn, or which implements the same `predict()` method as scikit-learn models (eg. xgboost).

## Installing

`pip install scikit-deploy`

## Configuration

First, you will need a model trained using scikit-learn 0.20 (should support all versions later on) which has been pickled.

You will also need a `configuration.json` file describing the model metadata and build information.
It takes the following form:

```
{
    "image_tag": "{{the tag given to the generated docker image}}",
    "endpoints": ["{{the endpoints to call for scoring}}"],
}
```

Endpoints have the following format:

```
{
    "route": "{{the HTTP route to call for scoring}}",
    "model_path": "{{model absolute path}}",
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
    "endpoints": [
        {
            "route": "/super-score",
            "model_path": "/home/toto/model.pkl",
            "inputs": [{"name": "x"}, {"name": "y", "default": 1.551, "offset": 50, "scaling": 2}],
            "outputs": [{"name": "z", "offset": 3, "scaling": 1.4}]
        }
    ],

}
```

## Building your image

Run the following command:

`skdeploy -c /path/to/config.json`

This will run a Docker build using the image name you have provided.

If your models require extra dependencies, you can specify an additional `requirements.txt` file to include
for your server with the `-r`flag:

`skdeploy -c /path/to/config -r /path/to/requirements.txt`

If you need to specify a SSH private key in case your requirements are part of a private repository, use the `-k` flag:

`skdeploy -c /path/to/config -r /path/to/requirements.txt -k "$(cat /path/to/private_key)"`


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
