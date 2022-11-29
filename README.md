<img src="./logo.png" height=100 align=right>

# YTStars

YTStars was made to ease the pains of manual comment analysis among content creators and viewers to find out how good a video is.
Here's it in a more relatable way:

Imagine you are looking for how to use and make APIs, some tutorial like:

<a href="https://www.youtube.com/watch?v=GZvSYJDk-us"><img src="https://i.ytimg.com/vi/GZvSYJDk-us/hq720.jpg" height=150></a>

You aren't really sure what to expect from the tutorial since it's over 2 hours long and covers a slightly specific topic. Sure, reading the first 10 comments may give you a general idea, but it's not necessarily covering all opinions.

With this tool, all the video comments are aggregated, analyzed for sentiment, and displayed in the most simple way - a rating.

Do you want to scavenge all those comments now?

# Setup

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

Start the infrastructure with `docker-compose`:

```bash
docker-compose up -d
```

> Currently, the intern

## Data pipelines

> **Notice**: These pipelines will soon use web APIs which are orchestrated under Docker rather than local APIs. For now, follow this section with `docker-compose` running.

Download comments from a video with no modifications:

```bash
python3 -m utils.comments GZvSYJDk-us 300 > output.json
```

Modify to include algorithm responses:

```bash
python3 -m utils.comments GZvSYJDk-us 20 | python3 -m src.algo.wrapper -tf --csv > future/poop.csv
```

`-t` runs TorchMoji, `-f` runs Flair, and `--csv` toggles CSV output

Fix them, if required:

```bash
./scripts/fix -f data.csv
```

> *This is currently not implemented*
