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

## Testing

Rateboat uses Amazon product reviews as a method of testing the algorithms.

Before you start screaming in pain about copy and pasting all these reviews, you can use a userscript I made [here](./future/copyReviews.js). It essentially functions as a macro to copy every review on a page for a number of pages.

You can install it with [Tampermonkey](https://www.tampermonkey.net/) and use it on a product review page like [this one](https://www.amazon.com/Samsung-Galaxy-G973U-128GB-T-Mobile/product-reviews/B07T8CN8WZ). Just make sure these URL parameters exist:

```text
?ie=UTF8&reviewerType=all_reviews&pageNumber=1&pageMacro=3 (&noChunk)
```

- `reviewerType` defines which reviews with ratings to collect
- `pageNumber` defines which page to start at
- `pageMacro` - part of the script - defines which page to stop scraping at
- `noChunk` also exists to stop the reviews from being chunked into groups of 5 (just in case)

Once finished, it will write all the reviews to the body so you can copy it.
