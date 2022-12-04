# Web API

A queue-based RESTful API which abstracts the complex data collection and processing logic YTStars uses.

Start the infrastructure with `docker compose`:

```bash
docker compose up -d
```

Since the front-facing API is currently not Dockerized, this must be run locally.

```bash
pip install fastapi pika 'uvicorn[standard]'
uvicorn src.web.application:app
```

This should be available in the browser at [http://localhost:8000](http://localhost:8000).

## Usage

### Generated client

If you are confused where to begin working with the API, you can generate a strongly-typed client from the OpenAPI spec in your desired programming language.

#### Python

We recommend using [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) since it generates a far less overwhelming client library than [`openapi-generator`](https://github.com/OpenAPITools/openapi-generator), which we mention later.

Create a virtual environment and install `openapi-python-client`:

```bash
python3 -m venv venv
. venv/bin/activate
pip install openapi-python-client
```

Generate a Python client from the OpenAPI spec:

```bash
openapi-python-client generate --url http://localhost:8000/openapi.json
```

You should now have a barebones library with access to modern Python features like type hinting and asyncio.

#### Other languages

Since `openapi-python-client` obviously doesn't have support for other languages, you can use `openapi-generator` for all of [these languages](https://github.com/OpenAPITools/openapi-generator#overview).

You can use the pre-built Docker image for this since doesn't require any dependencies.

```bash
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i http://localhost:8000/openapi.yaml \
    -g <language> \
    -o /local/client
```

Replace &lt;language&gt;
