# ytstars
Rate YouTube videos based on comments

## Requirements
- Python 3 (entire app codebase)
- Docker (optional but good for scaling)

## Usage

Clone the repository with `--depth=1` because there is a large file in the Git history and it would take years to download without the flag.
```bash
git clone --depth=1 https://github.com/themysticsavages/ytstars
cd ytstars
```

Get prerequisites:
```bash
pip install -r requirements.txt
# download torchmoji model
./manage dlmodel
```

Start the API locally:
```bash
uvicorn src:app
```

Heading to http://localhost:8000 should give you `"Pong.\n"`

You can also start this up with Docker Compose:
```bash
docker-compose up
```