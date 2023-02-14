<img src="./media/logo.svg" width=130 align=right />

# Wordsmyth

Wordsmyth is a free and open-source tool to ease the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, Wordsmyth **generates them** based on the **text sentiment** using a pair of models and well-tested output finetuning.

## Highlights

- Works on almost any platform and very easy to extend
- 85-100% accuracy (tested against Amazon reviews) and sometimes more accurate than user ratings
- Accessible to anybody (planned browser extension, web dashboard, API, and command line)

## Status

Wordsmyth recently had a refactor to simplify the codebase and may continue to refactor, so expect changes to the documentation. Technically it is feature complete, but not production-ready.

## Usage

Wordsmyth is currently available as a pipeline to load comments from a data source and output star ratings.

Install the pre-requisites:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./helper model
```

You can now download some comments to test the pipeline. For instance, with the provided YouTube comment script:

```bash
python3 scripts/comments.py | jq > comments.json
```

Then pass the comments into either the `RateTable` or `RatePlot` pipeline:

```bash
python3 evaluate_comments.py RateTable --comments example.json
```

`RateTable` prints the head and tail of the evaluated reviews and prints a summary of the data. `RatePlot` generates an interactive plot of the evaluated reviews like below:

<div align=center>
    <img src="./media/review_plot.png" alt="Review plot">
</div><br>

Both of these pipelines use [Pickle](https://docs.python.org/3/library/pickle.html) files to persist the output data to be cached easily.
