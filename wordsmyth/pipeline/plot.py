from pandas import DataFrame

import plotly.express as px
from plotly.graph_objs._figure import Figure


def scatter_comments(data: DataFrame) -> Figure:
    data = data.drop_duplicates(["text"]).reset_index(drop=True)

    fig = px.density_heatmap(
        data,
        x="overall",
        y="rating",
        text_auto=True,
    )
    fig.update_yaxes(range=[1, 5])
    fig.update_xaxes(range=[1, 5])

    return fig
