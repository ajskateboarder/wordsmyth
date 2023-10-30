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

Install the requisites:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./helper model # downloads the TorchMoji model locally
```

and use the module like so:

```py
import wordsmyth

model = wordsmyth.Pipeline()
content = model("LOL")
print(content, "stars") # 5 stars

content.metadata # rating process info
```

There are also scripts to download reviews and benchmark this algorithm in `scripts/`.

## Desktop app

This provides a GUI for Wordsmyth and allows users to analyze Amazon products, This app is not completely functional yet as there is no bundled version of Wordsmyth to use. However, here are instructions for building and running the app:

```bash
cd desktop
pnpm i
pnpm tauri dev
```

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
