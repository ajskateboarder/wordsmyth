<img src="./logo.png" height=100 align=right>

# YTStars

YTStars was made to ease the pains of manual comment analysis among content creators and viewers to find out how good a video is.
Here's it in a more relatable way:

Imagine you are looking for how to use and make APIs, some tutorial like:

<a href="https://www.youtube.com/watch?v=GZvSYJDk-us"><img src="https://i.ytimg.com/vi/GZvSYJDk-us/hq720.jpg" height=150></a>

You aren't really sure what to expect from the tutorial since it's over 2 hours long and covers a slightly specific topic. Sure, reading the first 10 comments may give you a general idea, but it's not necessarily covering all opinions.

With this tool, all the video comments are aggregated, analyzed for sentiment, and displayed in the most simple way - a rating.

Do you want to scavenge all those comments now?

## Status

YTStars is currently in development and all features haven't been implemented (no rating). Currently, we have:

- a finished server for handling concurrent requests to algorithms
- data pipelines for comments and algos on the said server
- a hacky script for making comment ratings (`future/verylast.py`)

Please read the [TODO.md](./TODO.md) for what still needs to be implemented.

# Usage

## Requirements

- Python 3
- Docker
- Linux/WSL (only platform the app was tested on)

## Pre-requisites

Clone the repository with `--depth=1` because there is a large file in the Git history and it would take way too long to clone without the flag.

```bash
git clone --depth=1 https://github.com/themysticsavages/ytstars
cd ytstars
```

Start the infrastructure with `docker compose`:

```bash
docker compose up -d
```

## Manual data pipelines
If you don't want to start all of the bulky web infrastructure, you can freely experiment with the data from the command line with these pipelines.

Start the gRPC service only:

```bash
docker compose start -d ytstars.internal
```

Download comments from a video without any modifications (algo responses are required for every other step):

```bash
python3 -m utils.comments GZvSYJDk-us 300 > output.json
```

Download comments with algorithm responses:

```bash
python3 -m utils.comments GZvSYJDk-us 300 | python3 -m src.algorithms.wrapper -t -f --csv > output
```
`-t` includes responses from TorchMoji, `-f` includes responses from Flair, and `--csv` will toggle CSV output for better readability.

> 🛈 The final pipelines are currently not finished so this will change in the future

Fix the responses from the previous data:

```bash
python3 future/fix.py path/to/previous/data
```

This should build the fixed `data.json` in the `future` directory, which you can generate a star rating from:

```bash
python3 future/rate.py
```
