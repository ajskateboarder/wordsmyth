#

<div align="center">

<img src="https://github.com/themysticsavages/ytstars/blob/main/media/ytstars_logo.png?raw=1" height=200 width=900>

<i><br><br>Rate YouTube videos based on comments (yes the logo looks draft-y)</i>

![status](https://img.shields.io/badge/status-alpha-orange)
</div>

## Overview

YTStars was made to make finding videos where overall criticism can be made (tutorials, for example) much easier. It's goal is to obviously give videos a star rating.

The backbone of this project is Hugging Face's [PyTorch implementation](https://github.com/huggingface/torchMoji) of [DeepMoji](https://github.com/bfelbo/DeepMoji), which has a pre-trained model to predict emojis. However, I made some updates to the library to make it Python 3 compatible.

Since I didn't feel like digging into the torchMoji library, I got a usable API to use with the model from this [gist](https://gist.github.com/cw75/57ca89cfa496f10c7c7b888ec5703d7f#file-emojize-py).

Whatever comments the program gets is thanks to [youtube-comment-downloader](https://github.com/egbertbouman/youtube-comment-downloader), a fast and completely free extractor that actually works.

## Structure

```text
media/
    Github README content
future/
    Random stuff because I couldn't put it on a separate branch
src/
    algo/
        Model libraries
    microv2/
        GRPC-based API to process data
tests/
    Tests for APIs
```

## Requirements

- Python 3 (entire app codebase)
- Docker (required for demos)
- Makefile (optional but makes development very enjoyable)
- Linux/WSL (only platform the app was tested on)

## Usage

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

##

Since the completion of the GRPC microservice, we recommend using it as the original REST API will soon be deprecated.

Create interoperable stubs, if needed:

```bash
make proto
```

Start the server:

```bash
make grpc
```

Run it with an example client:

```bash
python3 future/client.py
```

### Dockerizing

Build and start the image with `docker-compose`:

```
docker-compose up -d
```

## Citations

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
