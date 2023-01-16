# Architecture

[![image](../media/architecture.png)](https://excalidraw.com/#json=_h4T0fdeQmFmGCZGr3jFI,2ycdaVkncvmdhzfuSICtCw)

- `rateboat-gui`: A frontend website with TypeScript and SvelteKit to submit content for review
- `rateboat-web`: A web API in Python with FastAPI
- `rateboat-store`: The outer protection layer for...
- `rateboat-internal`: The algorithm services which are used for analysis
- `auto-indexer`: A content crawler which submits to `rateboat-store`

The request initially comes from `rateboat-gui` when they want to index some content, whether it be from YouTube, Soundcloud, or any other supported platformers. 

Making requests to process videos is done with two Python gRPC services: one for handling the state of processing, `rateboat-store`, and another to actually process the data, `rateboat-internal`.

`rateboat-store` acts as a barrier to the inner service to prevent users from sending identical videos to be processed. 

This uses an in-memory state to keep track of what content is being processed and every request sent to the store is run in a new thread. This is most likely safe on memory and threads.

`rateboat-internal` hosts the algorithms needed for processing data, which you can find more info about [here](./docs/ALGORITHMS.md).

Upon receiving a request from `rateboat-store`, it will:

- generate the results by requesting `rateboat-internal`
- create an SSE route on `rateboat-web`
- push processing updates via that route

The results of `rateboat-store` is saved in a document database like RedisJSON or Firebase if I'm too lazy to self-host Redis.

`auto-indexer` is simply a web crawler to find new content and send requests directly to `rateboat-store` for indexing. This will certainly be split into multiple processes that run for every configured service.
