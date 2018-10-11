# scikit-deploy

Deploy models trained with scikit-learn with Docker.

## Requirements

You will require python 3 and Docker installed on your system.

## Installing

For now, clone the repo and run `python setup.py install`.
This will install the `skdeploy` CLI.

## Configuration

First, you will need a model trained using scikit-learn 0.20 (should support all versions later on) which has been pickled.

You will also need a `configuration.json` file describing the model metadata and build information.
It takes the following form:

```
{
    "image_tag": "{{the tag given to the generated docker image}}",
    "url_prefix": "{{optional, a prefix to give to the scoring endpoint}}",
    "inputs": [{{the names of the input features}}],
    "outputs": [{{the names of the output targets}}]
}
```

Here is an example config file :

```
{
    "image_tag": "my_super_model:latest",
    "url_prefix": "/v1",
    "inputs": ["x", "y"],
    "outputs": ["z"]
}
```

## Building your image

Run the following command:

`skdeploy /path/to/model/pickle /path/to/config.json`

This will run a Docker build using the image name you have provided.

## Running and testing the server

The server running inside the Docker container listens on port 5000.
To test your server on local port 8080 for example, run it using docker:

`docker run -p 8080:5000 your_image_tag`

And you can start querying the server ; for the config file above, this would be done as :

`GET localhost:8000/v1/score?x=1337&y=42`

Which would yield the json

```
{
    "prediction": {
        "z": 11525
    }
}
```
