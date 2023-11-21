<picture>
<source media="(prefers-color-scheme: dark)" srcset="./media/logo_dark.svg" width=130 align=right />
<img alt="The Wordsmyth logo" src="./media/logo.svg" align="right" width=130>
</picture>

# Wordsmyth

Wordsmyth eases the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, Wordsmyth *generates them* based on the text sentiment by applying pre-trained neural network results to deterministic rules. This combination of data analysis results in high-accuracy rating prediction that is mostly unbiased.

<div align="center">
<img src="./media/how_it_works.png">
</div>

Wordsmyth has relatively good performance across different types of content, from YouTube comments to Amazon reviews.

## Python

Download the TorchMoji model locally:

```bash
curl https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0 -L --output src/wordsmyth/data/pytorch_model.bin
```

Install the requisites:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

and use the module like so:

```py
from wordsmyth import rate

rating = rate("Hello world")
print(rating, "stars") # 5 stars

rating, flags = rate("Hello world", flags=True)
print(flags) # [content flags ...]
```

There are also scripts to download reviews and benchmark this algorithm in `scripts/`. (they need some updating though)

<!--
Not sure if this is an issue anymore, so it's commented :P

## Caveats

### Irregular tone shifts in sentiment

Text that quickly changes in tone can sometimes be incorrectly predicted by the algorithm stack, especially in the case of Flair.

An example of this type of text would include:

| content       | predicted     | actual |
| ------------- | ------------- | ------ |
| works great. we loved ours! till we didn't. these do not last so buy the warranty as you WILL NEED IT. | 4.3935 | 2
| Luved it for the few months it worked! great little bullet shaped ice cubes. It was a gift for my sister who never opened the box. The next summer during a heat wave I asked for my unused gift back, ha!, and was in heaven for a few months. the next summer after a few weeks the unit gave out... | 4.7115 | 2 |
-->
