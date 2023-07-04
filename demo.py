from __future__ import annotations

from typing import no_type_check
from statistics import mean

import streamlit as st
from scripts.amazon import AmazonScraper


@no_type_check
@st.cache_resource
def load_model():
    from wordsmyth import Pipeline  # pylint: disable=import-outside-toplevel

    return Pipeline()


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

data_collection, evaluation = st.columns(2, gap="large")


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
"""


def legend(percents: list[float], include_na: bool = True) -> str:
    l = len(percents) - 5
    return f"""<ul{" style='margin-top: 25px'" if not include_na else ""}>{f"<li><font size='2'><span style='color: #708090'>&#9679;</span> N/A ({percents[0]:.0%})</font></li>" if include_na else ""}
    <li><font size="2"><span style="color: #FF0000">&#9679;</span> 1 star ({percents[l]:.0%})</font></li>
    <li><font size="2"><span style="color: #FF5500">&#9679;</span> 2 stars ({percents[l+1]:.0%})</font></li>
    <li><font size="2"><span style="color: #FFAA00">&#9679;</span> 3 stars ({percents[l+2]:.0%})</font></li>
    <li><font size="2"><span style="color: #AAFF00">&#9679;</span> 4 stars ({percents[l+3]:.0%})</font></li>
    <li><font size="2"><span style="color: #00FF00">&#9679;</span> 5 stars ({percents[l+4]:.0%})</font></li>
</ul>
"""


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
    st.markdown("And this bar shows the predicted star ratings from those reviews:")
    prediction_bar = st.markdown(
        "<div style='background-color: #d8d8d8; width: 100%; height: 20px; position: relative;'></div>",
        unsafe_allow_html=True,
    )
    # st.markdown(legend([0.2, 0.3, 0.1, 0.2, 0.2], True), unsafe_allow_html=True)
    prediction_legend = st.markdown(
        PLACEHOLDER_LEGEND.format("", NA_PLACEHOLDER),
        unsafe_allow_html=True,
    )


with data_collection:
    st.markdown(
        """### Amazon reviews
This downloads a max of 100 written reviews from an Amazon product,
as Amazon caps reviews at 10 pages on the frontend."""
    )
    actual_results = []
    prediction_results = []

    with st.form("data_collection_form"):
        product = st.text_input(
            "Amazon product URL",
            "https://www.amazon.com/Samsung-Factory-Unlocked-Warranty-Renewed/dp/B07PB77Z4J",
        )

        submitted = st.form_submit_button("Download")
        if submitted:
            scraper = AmazonScraper(location="/usr/bin/firefox")

            for review in scraper._fetch_reviews(product.split("/")[-1], 10):
                prediction_results.append(model.predict(review["reviewText"]))

                actual_results.append(review["overall"])
                predictions = [
                    prediction_results.count(None) / len(prediction_results),
                    *[
                        prediction_results.count(i) / len(prediction_results)
                        for i in range(1, 6)
                    ],
                ]
                actuals = [
                    0,
                    *[
                        actual_results.count(i) / len(actual_results)
                        for i in range(1, 6)
                    ],
                ]
                with evaluation:
                    avg = round(
                        mean(filter(lambda x: x is not None, prediction_results)), 2
                    )
                    prediction_bar.markdown(
                        inline_bar(predictions) + str(avg),
                        unsafe_allow_html=True,
                    )
                    prediction_legend.markdown(
                        legend(predictions, True), unsafe_allow_html=True
                    )

                    avg = round(
                        mean(filter(lambda x: x is not None, actual_results)), 2
                    )
                    actual_bar.markdown(
                        inline_bar(actuals) + str(avg),
                        unsafe_allow_html=True,
                    )
                    actual_legend.markdown(
                        legend(actuals, False), unsafe_allow_html=True
                    )
