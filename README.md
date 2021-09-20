# AbBOT-api Overview

This project is used to generate anonymous randomized data and serve it up via a RESTful API to other AbBOT projects.

## Usage

### Customization

#### Environment Variables

Customization of the API and how it runs can be done through the following environment variables.

| Name             | Acceptable Values                              | Default     |
| ---------------- | ---------------------------------------------- | ----------- |
| `MODEL_NAME`     | `str` one of `"gpt2"`, `"4chan"`               | `"gpt2"`    |
| `API_BATCH_SIZE` | `int` greater than `0`                         | `5`         |
| `ALLOWED_APIS`   | `List[str]` (comma separated list or asterisk) | `"*"`       |
| `API_HOST`       | `str` IP address                               | `"0.0.0.0"` |
| `API_PORT`       | `int` port number                              | `5000`      |

- `MODEL_NAME` determines which model to use for generation of random text used by the APIs. <small>Warning: The 4Chan option is NSFW and should be used with caution.</small>
- `API_BATCH_SIZE` determines how many entries to generate from the model and put into the queue while the APIs are waiting for requests.
- `ALLOWED_APIS` determines which API paths will be loaded. For example, if the file was `api/generators/prolifewhistleblower.py` way I would load the APIs for only this one would be `ALLOWED_APIS="prolifewhistleblower"`
- `API_HOST` determines which interfaces to host the REST API on.
- `API_PORT` determines which TCP port to host the REST API on.

If you're not sure how to set environment variables in your environment, check out these guides and documentation:

- [Set environment variables - Docker](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) (Docker documentation)
- [Environment variable assignment - Unix](https://en.wikipedia.org/wiki/Environment_variable#Assignment:_Unix) (Wikipedia)
- [Enviornment variable assignment - Windows](https://en.wikipedia.org/wiki/Environment_variable#Assignment:_DOS,_OS/2_and_Windows) (Wikipedia)

### Usage with Docker

First, build the docker image.

```bash
docker image build -t dev-abbot-model .
```

After that, start the inference engine.

```bash
# Normal
docker container run -p 5000:5000 --rm dev-abbot-model

# Specify environment variables
docker container run -e MODEL_NAME='gpt2' -e API_BATCH_SIZE='5' -e ALLOWED_APIS='*' -e API_PORT='8080' -p 8080:8080 --rm dev-abbot-model
```

After the container starts up, you're ready to go.

### Usage with Python 3

#### Install Python

If you don't already have Python installed, you can check out [the Python Beginner's Guide's instructions for installation](https://wiki.python.org/moin/BeginnersGuide/Download).

After you have Python installed, make sure you have Pip installed by running the following command.

```bash
pip3 --version
# or
python3 -m pip --version
# or
python3 -m ensurepip --default-pip
```

If you don't have Pip installed, you can download [the `get-pip.py` script](https://bootstrap.pypa.io/get-pip.py) and run it with `python3`.

```bash
curl 'https://bootstrap.pypa.io/get-pip.py' -o ./get-pip.py
python3 ./get-pip.py
```

#### Installing dependencies

First we'll need to install Pipenv.

```bash
pip3 install --user pipenv
```

Then we can use `pipenv` to install all of the dependencies of this project.

```bash
pipenv install
```

#### Running the program

Before we can run the program, there's one script we need to run to download some runtime dependencies.

```bash
python3 ./download_weights.py
```

Now that all dependencies are installed and downloaded you can run the program (`main.py`) and set environment variables as you wish.

```bash
# Normal
python3 ./main.py
# or make it executable (Unix/Linux/macOS only)
chmod +x ./main.py
./main.py

# Specify environment variables (Bourne shell and related shells)
MODEL_NAME='gpt2' -e API_BATCH_SIZE='5' -e ALLOWED_APIS='*' API_PORT='8080' python3 ./main.py
# or set environment variables for whole session
export MODEL_NAME='gpt2' -e API_BATCH_SIZE='5' -e ALLOWED_APIS='*' API_PORT='8080'
python3 ./main.py
```

### Testing the API

You can test the API with a simple curl command. If you add `-i` you can also see the headers. Bear in mind that the text generation models will take several minutes to start up and fill up the queues.

```bash
curl http://localhost:5000/prolifewhistleblower/anonymous-form
```

#### Expected output format

##### Successful requests

The data will be sent back through the response body as JSON. This JSON is generated directly by each API point individually so the format will vary between API paths. For example, the following output is the output of the `curl -i http://localhost:5000/prolifewhistleblower/anonymous-form` command.

```http
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 624
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Sat, 11 Sep 2021 22:41:18 GMT

{
  "violation": "Dear Gov. Abbott, if you want a new bill to be read at all, we're getting it. It's all very well but now we have a bill that can't be read.\"\n\nMr. Abbott said he was happy that the measure that he introduced had passed.\n\n\"This would have been a much better bill,\" he said.\n\nWrite to John F. Stokes at john.stokes@wsj.com and David L. Bock at dave.bock@wsj.com",
  "obtained_evidence_from": "His wife told me",
  "clinic_or_doctor": "Dr. Trevor Hernandez",
  "city": "Aquilla",
  "state": "Texas",
  "zip_code": "76622",
  "county": "Hill",
  "ip_address": "67.10.46.59",
  "elected_to_public_office": "no"
}
```

##### An internal server error occurred

Currently the only error handling we have for issues with the API itself is an HTTP `500` catch-all. It will extract the error message from the actual error that occurred on the server and put it into a JSON object as `message`.

```http
HTTP/1.0 500 INTERNAL SERVER ERROR
Content-Type: application/json
Content-Length: 24
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Sat, 11 Sep 2021 22:57:01 GMT

{
  "message": "<Error message here>"
}
```

##### 404 API path not found

This one is pretty self-explanatory.

```http
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 53
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Sat, 11 Sep 2021 23:03:46 GMT

{
  "message": "The requested API path does not exist."
}
```

## Attribution

- Texas ZIP code data was obtained from [World Population Review](https://worldpopulationreview.com/zips/texas).

# Contributing

TODO: add instructions on how to contribute.

## Formatting

Before committing your code each time, please format your code with `yapf`. If you think the style should be different, please open an issue or PR about the `.style.yapf` file. VS Code can be configured to use `yapf` and so can other editors. If you do not have an editor with automatic formatting that supports `yapf`, you can use `yapf` directly with `yapf -ri .`.
