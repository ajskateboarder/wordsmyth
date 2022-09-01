#

<div align="center">

<img src="https://github.com/themysticsavages/ytstars/blob/main/media/ytstars_logo.png" height=200 width=900>

<i><br><br>Rate YouTube videos based on comments (yes the logo looks draft-y)</i>

![status](https://img.shields.io/badge/status-alpha-orange)
</div>

## Overview

YTStars was made to make finding videos where overall criticism can be made (tutorials, for example) much easier. It's goal is to obviously give videos a star rating.

The backbone of this project is Hugging Face's [PyTorch implementation](https://github.com/huggingface/torchMoji) of [DeepMoji](https://github.com/bfelbo/DeepMoji), which has a pre-trained model to predict emojis. However, I made some updates to the library to make it Python 3 compatible.

Since I didn't feel like digging into the torchMoji library, I got a usable API to use with the model from this [gist](https://gist.github.com/cw75/57ca89cfa496f10c7c7b888ec5703d7f#file-emojize-py).

Whatever comments the program gets is thanks to [youtube-comment-downloader](https://github.com/egbertbouman/youtube-comment-downloader), a fast and completely free extractor that actually works.

## Structure

This only contains top level folders for simplicity.

```text
citations/
    Any citations the project uses
media/
    Github README content
scripts/
    Scripts to abstract Docker scaling
src/
    deepmoji/
        Model library
    micro/
        Microservice to multiprocess comments
    ytd/
        Small wrapper over youtube-comment-downloader
```

## Requirements

- Python 3 (entire app codebase)
- Docker (required for demos)
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

Start the comment processing microservice locally:

```bash
uvicorn src.micro.main:app
```

Heading to [http://localhost:8000](http://localhost:8000) should give you `"Pong.\n"`

### Scaling

Build the Docker image from the Dockerfile:

```bash
# prepend DOCKER_BUILDKIT=1 to apply better caching and faster build times
docker build -t myimage .
```

Scale the API for faster processing of comments:

```bash
make scale image=myimage
# ./scripts/scale myimage
```

After running `docker ps`, you should see these containers listed:

```text
PORTS                                       NAMES
0.0.0.0:8005->8005/tcp, :::8005->8005/tcp   econ5
0.0.0.0:8004->8004/tcp, :::8004->8004/tcp   econ4
0.0.0.0:8003->8003/tcp, :::8003->8003/tcp   econ3
0.0.0.0:8002->8002/tcp, :::8002->8002/tcp   econ2
0.0.0.0:8001->8001/tcp, :::8001->8001/tcp   econ1
```

Kill the containers when you are done with them:

```bash
make killcons
# ./scripts/killcons
```