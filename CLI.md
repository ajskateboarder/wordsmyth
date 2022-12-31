# Manual data pipelines

If you don't want to start all of the bulky web infrastructure, you can freely experiment with the data from the command line with these pipelines.

Start the gRPC service only:

```bash
docker compose start -d rateboat.internal
```

Download comments from a video without any modifications (algo responses are required for every other step):

```bash
python3 -m utils.comments GZvSYJDk-us 300 > output.json
```

Download comments with algorithm responses:

```bash
python3 -m utils.comments GZvSYJDk-us 300 | python3 -m src.algorithms.wrapper -t -f --csv > output
```

`-t` includes responses from TorchMoji, `-f` includes responses from Flair, and `--csv` will toggle CSV output for better readability.

> ℹ️ The final pipelines are currently not finished so this will change in the future.

Fix the responses from the previous data:

```bash
python3 future/fix.py path/to/previous/data
```

This should build the fixed `data.json` in the `future` directory, which you can generate a star rating from:

```bash
python3 future/rate.py
```

## Testing usage

This program uses Amazon product reviews as a method of testing the algorithms. Since you and I are probably too lazy to copy each review to use with RateBoat
