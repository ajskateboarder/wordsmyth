# Web API

A queue-based RESTful API which abstracts the complex data collection and processing logic Rateboat uses.

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

A queue-based RESTful API which abstracts the complex data collection and processing logic rateboat uses.

## Explanation

![image](https://github.com/ajskateboarder/stuff/blob/main/flowchart.png?raw=true)

Making requests to process videos is done with two gRPC services: one for handling the state of processing and another to actually process the data.

The first and outer service acts as a barrier to the inner service to prevent users from sending identical videos to be processed. This takes advantage of Redis to store videos as a queue since it's blazingly fast. 

(The outer service previously used RabbitMQ while it was obviously not required)

If a requested video isn't being processed already, it will download ~300 comments from that video, break them into small chunks, and send each chunk as a request in parallel to the inner service (where all the fun happens!)

The inner service hosts the algorithms needed for processing data, which you can find more info about [here](./docs/ALGORITHMS.md). 

Upon receiving a request from the outer service, it will request to generate an [SSE](https://en.wikipedia.org/wiki/Server-sent_events) route directly on the public API to push processing updates and results to the client, which you can see on the flowchart. Then the service will do its necessary work and push the final results to a database (preferably a NoSQL type) so it can easily be requested by users in the future.

