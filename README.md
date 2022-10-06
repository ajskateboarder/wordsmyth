<div align="center">

<img src="https://github.com/themysticsavages/ytstars/blob/main/logo.png?raw=1" height=100 width=400>

<i><br>Rate YouTube videos based on comments (yes the logo looks draft-y)</i>

![status](https://img.shields.io/badge/status-alpha-orange)
</div>

#

## Overview

YTStars was made to ease the pains of manual comment analysis among content creators and viewers to find out how good a video is.
Here's it in a more relatable way:

Imagine you are looking for how to use and make APIs, some tutorial like:

<a href="https://www.youtube.com/watch?v=GZvSYJDk-us"><img src="https://i.ytimg.com/vi/GZvSYJDk-us/hq720.jpg" height=150></a>

You aren't really sure what to expect from the tutorial since it's over 2 hours long and covers a slightly specific topic. Sure, reading the first 10 comments may give you a general idea, but it's not necessarily covering all opinions.

With this tool, all the video comments are aggregated, analyzed for sentiment, and displayed in the most simple way - a rating.

Do you want to scavenge all those comments now?

# Usage

## Requirements

- Python 3 (entire app codebase)
- Docker (required for demos)
- Makefile (optional but makes development very nice)
- Linux/WSL (only platform the app was tested on)

## Pre-requisites

Clone the repository with `--depth=1` because there is a large file in the Git history and it would take way too long to clone without the flag.

```bash
git clone --depth=1 https://github.com/themysticsavages/ytstars
cd ytstars
pip install -r requirements.txt
```

Get the torchMoji model:

```bash
make dlmodel
```

If you do not have [wget](https://www.gnu.org/software/wget) installed, get the model from [here](https://dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0) and save it in `src/deepmoji/model/`.

Since the completion of the GRPC microservice, we recommend using it as the original REST API will soon be deprecated.

Create interoperable stubs, if needed:

```bash
make proto
```

Start the server:

```bash
make grpc
```

or with `docker-compose`:

```bash
docker-compose up -d
```

## Data pipelines



```

Download comments from a video with no modifications:

```bash
./tools/comments GZvSYJDk-us 300 > output.json
```

Modify to include algorithm responses:

```bash
./tools/comments GZvSYJDk-us 300 | ./pipe/algo -t -f
# -t runs TorchMoji, -f runs Flair
```

Fix them, if required:

```bash
./scripts/fix -f data.csv
```

# Citations

```bibtex
@inproceedings{felbo2017,
  title={Using millions of emoji occurrences to learn any-domain representations for detecting sentiment, emotion and sarcasm},
  author={Felbo, Bjarke and Mislove, Alan and S{\o}gaard, Anders and Rahwan, Iyad and Lehmann, Sune},
  booktitle={Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year={2017}
}
```

```bibtex
@article{Kralj2015emojis,
  author={{Kralj Novak}, Petra and Smailovi{\'c}, Jasmina and Sluban, Borut and Mozeti\v{c}, Igor},
  title={Sentiment of emojis},
  journal={PLoS ONE},
  volume={10},
  number={12},
  pages={e0144296},
  url={http://dx.doi.org/10.1371/journal.pone.0144296},
  year={2015}
}
```
