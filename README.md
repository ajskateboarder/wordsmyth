<div align="center">
<img src="https://github.com/themysticsavages/ytstars/blob/main/media/ytstars_logo.png" height=200 width=900>

<i>Rate YouTube videos based on comments (i know the logo's kinda crappy it's just a draft)</i>
</div>

## Requirements

- Python 3 (entire app codebase)
- Docker (required for demos)
- Linux/WSL (only platform the app was tested on)

## Usage

Clone the repository with `--depth=1` because there is a large file in the Git history and it would take years to download without the flag.

```bash
git clone --depth=1 https://github.com/themysticsavages/ytstars
cd ytstars
pip install -r requirements.txt
```

Get the torchMoji model:

```bash
make dlmodel
```

If you do not have [wget](https://www.gnu.org/software/wget/) installed, get the model from [here](https://dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0) and save it to `src/deepmoji/model`.

Start the comment processing microservice locally:

```bash
uvicorn src.api.main:app
```

Heading to [http://localhost:8000](http://localhost:8000) should give you `"Pong.\n"`

### Scaling

Build the Docker image from the Dockerfile:

```bash
docker build -t myimage .
```

Scale the API for faster processing of comments:

```bash
make scale image=myimage
```

Or use it without make:

```bash
bash scripts/scale.sh myimage
```

After running `docker ps`, you should see these containers:

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
```

Or its alternative:

```bash
bash scripts/killcons.sh
```
