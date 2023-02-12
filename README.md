<img src="./media/logo.svg" width=130 align=right />

# Wordsmyth

> **Note**:
> This is a minimal rewrite of Wordsmyth's main branch to make it less complex. Please visit branch `main` to see the current source code.

Wordsmyth is a free and open-source tool to ease the pains of manual comment analysis among content creators and users.

Instead of relying on star ratings given by the user, Wordsmyth **generates them** based on the **text sentiment** using a pair of models and well-tested output finetuning.

## Highlights

- Works on almost any platform and very easy to extend
- 85-100% accuracy (tested against Amazon reviews) and sometimes more accurate than user ratings
- Accessible to anybody (planned browser extension, web dashboard, API, and command line)

## Usage

Wordsmyth is available as a pipeline to load comments from a data source and output star ratings.

Install the pre-requisites:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./helper model
```

Assuming you have a list of comments stored somewhere as JSON, run the pipeline:

```bash
python3 evaluate_comments.py RateComments --comments example.json
```
