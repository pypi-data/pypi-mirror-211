"""Module for converting input figure into Econoplots style."""
# %% Imports

# Standard Library Imports
from copy import deepcopy

# Third Party Imports
from matplotlib import pyplot as plt  # noqa
from matplotlib.axes import Axes

# Econoplots Imports
from econoplots.params import setRCParams
from econoplots.utils import (
    loadColorMap,
    makePatchSpinesInvisible,
    replaceAxesMinusGlyphs,
    setDefaultLineColors,
    setDefaultXAxisParams,
    setDefaultYAxisParams,
)

# %% Load color map and set parameters
setRCParams()

# with open("econoplots/color_map.json") as json_file:
#     color_map = json.load(json_file)

# %% Functions


def convert2Econo(ax: Axes) -> Axes:
    assert isinstance(ax, Axes)
    color_map = loadColorMap()

    # Change axis color
    ax.grid(
        which="major",
        axis="y",
        color=color_map["grid"]["grid_gray"],
        zorder=1,
    )

    # Change line colors
    setDefaultLineColors(ax)

    # set axis params
    y_offset_text = ax.yaxis.get_offset_text().get_text()
    x_offset_text = ax.xaxis.get_offset_text().get_text()
    replaceAxesMinusGlyphs(ax)
    setDefaultYAxisParams(ax, side="right", label_location="right")
    setDefaultXAxisParams(ax, pad_side="right", minor_ticks_on=True)

    # delete top, right, left spines
    makePatchSpinesInvisible(ax, ["top", "right", "left"])

    return ax
