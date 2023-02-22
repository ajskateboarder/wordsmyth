from pandas import DataFrame

import seaborn as sns
from seaborn.axisgrid import FacetGrid

DARK_PLOT = {
    "axes.facecolor": "black",
    "figure.facecolor": "black",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#303030",
}


def catplot_comments(data: DataFrame, dark: bool = False) -> FacetGrid:
    """Create a categorical plot of the complete data"""

    data = data.drop_duplicates(["text"]).reset_index(drop=True)

    if dark:
        sns.set(rc=DARK_PLOT)

    return (
        sns.catplot(data, x="overall", y="rating", palette="pastel", hue="overall")
        .set_axis_labels("Actual rating", "Predicted rating")
        .set(xlim=(-1, 5), ylim=(0, 6))
    )
