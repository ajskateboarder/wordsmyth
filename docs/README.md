# Architecture

[![image](../media/architecture.png)](https://excalidraw.com/#json=_h4T0fdeQmFmGCZGr3jFI,2ycdaVkncvmdhzfuSICtCw)

- `wordsmyth-gui`: A frontend website with TypeScript and SvelteKit to submit content for review
- `wordsmyth-web`: A web API in Python with FastAPI
- `wordsmyth-store`: The outer protection layer for...
- `wordsmyth-internal`: The algorithm services which are used for analysis
- `auto-indexer`: A content crawler which submits to `wordsmyth-store`

The request initially comes from `wordsmyth-gui` when they want to index some content, whether it be from YouTube, Soundcloud, or any other supported platformers. 

Making requests to process videos is done with two Python gRPC services: one for handling the state of processing, `wordsmyth-store`, and another to actually process the data, `wordsmyth-internal`.

`wordsmyth-store` acts as a barrier to the inner service to prevent users from sending identical videos to be processed. 

This uses an in-memory state to keep track of what content is being processed and every request sent to the store is run in a new thread. This is most likely safe on memory and threads.

`wordsmyth-internal` hosts the algorithms needed for processing data, which you can find more info about [here](./docs/ALGORITHMS.md).

Upon receiving a request from `wordsmyth-store`, it will:

- generate the results by requesting `wordsmyth-internal`
- create an SSE route on `wordsmyth-web`
- push processing updates via that route

The results of `wordsmyth-store` is saved in a document database like RedisJSON or Firebase if I'm too lazy to self-host Redis.

`auto-indexer` is simply a web crawler to find new content and send requests directly to `wordsmyth-store` for indexing. This will certainly be split into multiple processes that run for every configured service.
