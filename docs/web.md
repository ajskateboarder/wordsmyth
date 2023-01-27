# Web API

A queue-based RESTful API which abstracts the complex data collection and processing logic Wordsmith uses.

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

The API is compliant with the OpenAPI spec, so you can use a client generator like [`openapi-generator`](https://github.com/OpenAPITools/openapi-generator).
