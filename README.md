# ytstars
Rate YouTube videos based on comments

## Requirements
- Python 3 (entire app codebase)
- Docker (browser container stuff)

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

Pull the standalone-chrome image down from Docker and start it:
```bash
docker pull selenium/standalone-chrome
# may require sudo
docker run --rm -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome
```

