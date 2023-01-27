<img src="./media/logo.svg" width=100 align=right />

# Wordsmith

[![Docker build status](https://github.com/themysticsavages/wordsmith/workflows/Docker%20build/badge.svg)](https://github.com/themysticsavages/wordsmith/actions/)

Wordsmith is a free and open-source tool to ease the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, WordSmith **generates them** based on the **text sentiment** using a pair of models and well-tested output finetuning.

<img src="https://img.shields.io/badge/%20-Get%20for%20Chrome-grey?&logo=google-chrome" height=25> <img src="https://img.shields.io/badge/%20-Get%20for%20Firefox-grey?&logo=firefox" height=25>

## Highlights

- Works on almost any platform and very easy to extend
- 85-100% accuracy (tested against Amazon reviews)
- Accessible to anybody (browser extension, web dashboard, API, and command line)

## Status

Wordsmith is currently in development and doesn't have a public API or a frontend, but it is stable for local use.

Please read the [`TODO.md`](./TODO.md) for specific things that still need to be implemented.

# Usage

Wordsmith is available as a browser extension, self-hostable web API, and a command line application. Every quickstart except for the extensions use Docker, and you might want to install it!

## Web API

You can spawn all the infrastructure with the prebuilt images on `ghcr.io` without cloning anything:

```bash
curl https://raw.githubusercontent.com/themysticsavages/wordsmith/\
     main/docker-compose.images.yml
docker compose up -f docker-compose.images.yml -d --build
```

or build and run it yourself:

```bash
git clone https://github.com/themysticsavages/wordsmith --depth=1
cd wordsmith
docker compose up -d --build
```

You should be able to queue an endpoint from the web API:

```bash
$ curl -X POST http://localhost:8081/youtube/queue \
     -H "Content-Type: application/json" \
     --data '{"video_id": "Rg8-9nc-y-U"}'
{"status": "success"}
```

## Command line
