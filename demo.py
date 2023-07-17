from __future__ import annotations

from typing import no_type_check
from statistics import mean, StatisticsError

import streamlit as st
from scripts.amazon import AmazonScraper
from scripts.amazon_more import AmazonScraper as AmazonParallelScraper

st.set_page_config(page_title="Wordsmyth demo")


@no_type_check
@st.cache_resource()
def load_model():
    from wordsmyth import Pipeline  # pylint: disable=import-outside-toplevel

    pipe = Pipeline()
    return pipe


model = load_model()

st.markdown(
    """# Wordsmyth demo ✨🖊️

Rate an Amazon product using a novel sentiment analysis approach.
This does not use existing star ratings, but rather the sentiment of
the content, which can often give more accurate ratings than consumers.
"""
)
st.markdown(
    """
    <style>
        ul {
            list-style-type: none;
            list-style: none;
            padding-left: 0;
            padding: 0;
            margin: 0;
            margin-top: 35px;
        }
        li {
            line-height: 0.8em;
            display: block;
            float: left;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

data_collection, evaluation = st.columns(2)


def inline_bar(percents: list[float]) -> str:
    width = list(map(lambda w: int(w * 100), percents))
    return f"""
<div style="width: 100%; height: 20px; position: relative;">
    <div style="background-color: #708090; width: {width[0]}%; height: 100%; position: absolute;"></div>
    <div style="background-color: #FF0000; width: {width[1]}%; height: 100%; position: absolute; left: {width[0]}%"></div>
    <div style="background-color: #FF5500; width: {width[2]}%; height: 100%; position: absolute; left: {width[0] + width[1]}%;"></div>
    <div style="background-color: #FFAA00; width: {width[3]}%; height: 100%; position: absolute; left: {width[0] + width[1] + width[2]}%;"></div>
    <div style="background-color: #AAFF00; width: {width[4]}%; height: 100%; position: absolute; left: {width[0] + width[1] + width[2] + width[3]}%;"></div>
    <div style="background-color: #00FF00; width: {width[5]}%; height: 100%; position: absolute; left: {width[0] + width[1] + width[2] + width[3] + width[4]}%;"></div>
</div>
"""  # noqa: E501


def legend(percents: list[float], include_na: bool = True) -> str:
    l = len(percents) - 5
    return f"""<ul{" style='margin-top: 25px'" if not include_na else ""}>{f"<li><font size='2'><span style='color: #708090'>&#9679;</span> N/A ({percents[0]:.0%})</font></li>" if include_na else ""}
    <li><font size="2"><span style="color: #FF0000">&#9679;</span> 1 star ({percents[l]:.0%})</font></li>
    <li><font size="2"><span style="color: #FF5500">&#9679;</span> 2 stars ({percents[l+1]:.0%})</font></li>
    <li><font size="2"><span style="color: #FFAA00">&#9679;</span> 3 stars ({percents[l+2]:.0%})</font></li>
    <li><font size="2"><span style="color: #AAFF00">&#9679;</span> 4 stars ({percents[l+3]:.0%})</font></li>
    <li><font size="2"><span style="color: #00FF00">&#9679;</span> 5 stars ({percents[l+4]:.0%})</font></li>
</ul>
"""  # noqa: E501


NA_PLACEHOLDER = (
    "\n<li><font size='2'><span style='color: #708090'>&#9679;</span> N/A</font></li>"
)
PLACEHOLDER_LEGEND = """<ul{}>{}
        <li><font size="2"><span style="color: #FF0000">&#9679;</span> 1 star</font></li>
        <li><font size="2"><span style="color: #FF5500">&#9679;</span> 2 stars</font></li>
        <li><font size="2"><span style="color: #FFAA00">&#9679;</span> 3 stars</font></li>
        <li><font size="2"><span style="color: #AAFF00">&#9679;</span> 4 stars</font></li>
        <li><font size="2"><span style="color: #00FF00">&#9679;</span> 5 stars</font></li>
    </ul>"""


with evaluation:
    st.markdown(
        """### Rating
Results will show up here when you click the "Download" button.
The following bar shows the actual ratings of each Amazon product review:
"""
    )
    actual_bar = st.markdown(
        "<div style='background-color: #d8d8d8; width: 100%; height: 20px; position: relative;'></div>",
        unsafe_allow_html=True,
    )
    actual_legend = st.markdown(
        f"""{PLACEHOLDER_LEGEND.format(" style='margin-top: 30px'", "")}""",
        unsafe_allow_html=True,
    )
    st.markdown(
        "And this bar shows the predicted star ratings using the emojis expressed in those reviews:"
    )
    prediction_bar = st.markdown(
        "<div style='background-color: #d8d8d8; width: 100%; height: 20px; position: relative;'></div>",
        unsafe_allow_html=True,
    )
    prediction_legend = st.markdown(
        PLACEHOLDER_LEGEND.format("", NA_PLACEHOLDER),
        unsafe_allow_html=True,
    )


def find_asin(url: str) -> str:
    """Find a product ASIN in a URL"""
    path = url.split("/")
    if "?" in path[-1]:
        return path[-2]
    if not path[0] == "https:":
        return url
    return path[-1]


def process_review(review: dict) -> None:
    prediction_results.append(model.predict(review["reviewText"]))

    actual_results.append(review["overall"])
    predictions = [
        prediction_results.count(None) / len(prediction_results),
        *[prediction_results.count(i) / len(prediction_results) for i in range(1, 6)],
    ]
    actuals = [
        0,
        *[actual_results.count(i) / len(actual_results) for i in range(1, 6)],
    ]
    with evaluation:
        try:
            avg = round(mean(filter(lambda x: x is not None, prediction_results)), 2)
        except StatisticsError:
            avg = 0

        prediction_bar.markdown(
            inline_bar(predictions) + str(avg),
            unsafe_allow_html=True,
        )
        prediction_legend.markdown(legend(predictions, True), unsafe_allow_html=True)

        avg = round(mean(filter(lambda x: x is not None, actual_results)), 2)
        actual_bar.markdown(
            inline_bar(actuals) + str(avg),
            unsafe_allow_html=True,
        )
        actual_legend.markdown(legend(actuals, False), unsafe_allow_html=True)


with data_collection:
    # If "Use less data" is unticked, this will download 500 written reviews from an Amazon product.
    # An Amazon email and password is required for review-specific operations.
    # Otherwise, this will download 100 reviews - the maximum number of publically available reviews.
    st.markdown(
        """### Amazon reviews
By default, 100 random reviews (10 pages) are selected from a product review page."""
    )
    actual_results = []
    prediction_results = []

    use_more = st.checkbox(
        "Use more data",
        help="Use this for a larger sample size than 100 reviews",
    )
    use_even_more = st.empty()

    if use_more:
        st.write(
            """
Note that this will launch five browsers and consume reviews in a parallel,
which can result in heavy bandwidth usage. This also requires an Amazon account."""
        )
        use_even_more = st.checkbox(
            "Use even more data!!!",
            help="Use if you want to test model accuracy or if you don't care about the average Amazon rating",
        )  # type: ignore # ??
        if use_even_more:
            st.write("This downloads 500 reviews (50 pages)")

    loading = st.empty()
    with st.form("data_collection_form"):
        if use_more:
            username = st.text_input("Email/Phone number")
            password = st.text_input("Password", type="password")
        product = st.text_input(
            "Amazon product URL/ASIN",
            "https://www.amazon.com/Samsung-Factory-Unlocked-Warranty-Renewed/dp/B07PB77Z4J",
        )

        submitted = st.form_submit_button("Download")
        if submitted:
            product_id = find_asin(product)
            loading = st.markdown("Launching scraper...")

            USE_100 = not use_more and not use_even_more
            USE_PROP = use_more and not use_even_more
            USE_500 = use_even_more

            if USE_100:
                loading = st.markdown("Scraping reviews...")
                with AmazonScraper() as scraper:
                    for review in scraper.fetch_product_reviews(product.split("/")[-1]):  # type: ignore
                        process_review(review)
                st.stop()
            if USE_PROP:
                loading = st.markdown("Fetching product proportions...")
                with AmazonScraper(False) as scraper:
                    proportions = scraper.get_proportions(product_id)
                with AmazonParallelScraper(False) as scrapers:
                    loading = st.markdown("Logging scrapers in...")
                    scrapers.login(username, password)
                    loading = st.markdown("Scraping reviews...")
                    scrapers.scrape(product.split("/")[-1], process_review, proportions)  # type: ignore
                st.stop()
            if USE_500:
                with AmazonParallelScraper() as scrapers:
                    loading = st.markdown("Logging scrapers in...")
                    scrapers.login(username, password)
                    loading = st.markdown("Scraping reviews...")
                    scrapers.scrape(product.split("/")[-1], process_review)
