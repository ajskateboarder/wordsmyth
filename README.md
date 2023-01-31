<img src="./media/logo.svg" width=130 align=right />

# Wordsmyth

[![Docker build status](https://github.com/themysticsavages/wordsmyth/workflows/Docker%20build/badge.svg)](https://github.com/themysticsavages/wordsmyth/actions/)

![Get for Chrome](https://img.shields.io/static/v1?message=Get%20for%20Chrome&logo=google-chrome&labelColor=5c5c5c&color=5c5c5c&logoColor=white&label=%20)
![Get for Firefox](https://img.shields.io/static/v1?message=Get%20for%20Firefox&logo=firefox&labelColor=5c5c5c&color=5c5c5c&label=%20&logoColor=white)

Wordsmyth is a free and open-source tool to ease the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, Wordsmyth **generates them** based on the **text sentiment** using a pair of models and well-tested output finetuning.

## Highlights

- Works on almost any platform and very easy to extend
- 85-100% accuracy (tested against Amazon reviews)
- Accessible to anybody (browser extension, web dashboard, API, and command line)

## Status

Wordsmyth is currently in development and doesn't have a public API or a frontend, but it is stable for local use.

Please read the [`TODO.md`](./TODO.md) for specific things that still need to be implemented.

# Usage

This section is for self-hosting the services to do your own indexing. Every quickstart uses Docker, and you should [install it](https://docs.docker.com/engine/install/) for consistent behavior.

## Web API

Make sure you have a `.env` file in the same directory with API keys for the respective platforms you want to support. Leaving a key value blank will simply close the route. You can follow the `.env.sample` for what you should put.

You can spawn all the infrastructure with prebuilt images from GHCR without cloning anything:

```bash
curl "https://raw.githubusercontent.com/themysticsavages/wordsmyth/ \
     main/docker-compose.images.yml" > docker-compose.yml
docker compose up -d --build
```

or build and run it yourself:

```bash
git clone https://github.com/themysticsavages/wordsmyth --depth=1
cd wordsmyth
docker compose up -d --build
```

You should be able to queue an endpoint from the web API with either method:

```bash
$ curl -X POST http://localhost:8081/youtube/queue \
     -H "Content-Type: application/json" \
     --data '{"video_id": "Rg8-9nc-y-U"}'
{"status": "success"}
```

## Command line

Start the algorithm service from source:

```bash
docker compose up -d --build wordsmyth.internal
```

Then use an existing plugin in conjunction with `wordsmyth.algorithms.wrapper`. Here's an example with YouTube:

```bash
python3 -m wordsmyth.utils.comments qq-RGFyaq0U 10
```

```bash
10 comments
[["legendary"], 
["The fact that I just learned to play this without support made myself think that I'm a real OG"], 
["I didnt crie because of this music, i cried because of those memories behind the music"], 
["I kind of wish for this song to be deleted, not because I hate it. But because it makes me tear up so much from the good memories"], 
["I want to cry when I hear it..."]]
```

Replies are automatically ignored, so you won't get the same amount of comments as requested. The comment count is printed to `STDERR` to it doesn't get piped to other programs. Now pipe this into the algorithm wrapper.

```bash
python3 -m wordsmyth.utils.comments qq-RGFyaq0U 10 | \
 python3 -m wordsmyth.algorithms.wrapper --flair --torch --csv
```

| Flag  | Description |
| :---: | ----- |
| `--flair`  | Toggles Flair processing  |
| `--torch`  | Toggles TorchMoji processing  |
| `--csv`  | Toggles CSV conversion. The data is otherwise JSON  |

```csv
sentiment,score,text,emojis
pos,0.9964135,legendary,":100:,:muscle:,:sunglasses:,:relieved:,:ok_hand:,:smiling_imp:,:sweat_smile:,:raised_hands:,:information_desk_person:,:smirk:"
neg,0.8435976,I want to cry when I hear it...,":cry:,:broken_heart:,:pensive:,:sleepy:,:disappointed:,:sweat:,:sob:,:persevere:,:confused:,:notes:"
pos,0.88585466,"I kind of wish for this song to be deleted, not because I hate it. But because it makes me tear up so much from the good memories",":cry:,:broken_heart:,:sob:,:sleepy:,:sweat:,:confounded:,:tired_face:,:pensive:,:disappointed:,:persevere:"
neg,0.9959791,The fact that I just learned to play this without support made myself think that I'm a real OG,":broken_heart:,:cry:,:sob:,:sleepy:,:notes:,:pensive:,:sweat:,:disappointed:,:musical_note:,:persevere:"
pos,0.986511,"I didnt crie because of this music, i cried because of those memories behind the music",":musical_note:,:notes:,:raised_hands:,:sunglasses:,:smiling_imp:,:muscle:,:pray:,:ok_hand:,:100:,:sparkles:"
```

This will be Dockerized soon.
