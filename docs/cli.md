# Manual data pipelines

If you don't want to start all of the bulky web infrastructure, you can freely experiment with the data from the command line with these pipelines.

> **Note**
> The pipeline CLI might be Dockerized in the future.

Start the algorithm service from source and install required dependencies:

```bash
docker compose up -d --build wordsmyth.internal
pip install -e . grpcio grpcio_tools
```

Then use an existing plugin in conjunction with `wordsmyth.algorithms.wrapper`. Here's an example with YouTube:

```bash
# C418 - Minecraft - Minecraft Volume Alpha
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

Now pipe this into the algorithm wrapper.

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

## Testing

Wordsmyth uses Amazon product reviews as a method of testing the non-ML algorithms. The data we use in particular is the 5-core subsets from the [2018 Amazon reviews](https://nijianmo.github.io/amazon/#subsets).

Applying Flair and Torch over reviews takes a long time (47 min on ~2.2k reviews), so the static output data is recommended.
