"""Standalone plotting functions."""
# %% Imports
from __future__ import annotations

# Standard Library Imports
import json

# Third Party Imports
import matplotlib as mpl
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from numpy import absolute, linspace, ndarray

# econoplots Imports
from econoplots.utils import (
    makePatchSpinesInvisible,
    padXAxis,
    setDefaultYAxisParams,
)

# %% Load color map
with open("econoplots/color_map.json") as json_file:
    color_map = json.load(json_file)

# %% MPL Params
mpl.rcParams["font.sans-serif"] = "arial"
mpl.rcParams["font.family"] = "sans-serif"

# mpl.rcParams["font.fantasy"] = "CREAMPUFF"
# mpl.rcParams["font.family"] = "fantasy"

mpl.rcParams["lines.linestyle"] = "-"
mpl.rcParams["lines.linewidth"] = 3
# mpl.rcParams["axes.prop_cycle"] = cycler(color=cm_line_chart)
mpl.rcParams["axes.prop_cycle"] = cycler(color=color_map["line_chart"])
mpl.rcParams["figure.facecolor"] = "w"
mpl.rcParams["axes.facecolor"] = "w"


# %% Functions
def fancyLinePlot(
    x: ndarray,
    y: list[ndarray],
    shaded: list[ndarray] = None,
    x_ax_label: str = None,
    y_ax_label: str = None,
) -> Figure:
    """Fancy plot emulating The Economist style guide.

    Args:
        x (`ndarray`): X data
        y (`list`[`ndarray`]): Y data. Each entry must be same length as `x`.
        x_ax_label (`str`, optional): x-axis label. Defaults to None.
        y_ax_label (`str`, optional): y-axis label. Defaults to None.

    Returns:
        Figure: _description_
    """
    # mpl.rcParams["figure.facecolor"] = "w"
    # mpl.rcParams["axes.facecolor"] = "w"

    if type(y) != list:
        y = [y]

    if type(shaded) != list and shaded is not None:
        shaded = [shaded]

    # create figure
    fig, ax = plt.subplots(sharex=True)
    # set grid
    ax.grid(
        which="major",
        axis="y",
        color=color_map["grid"]["grid_gray"],
        zorder=1,
    )
    # ax.grid(which="major", axis="y", color="#B7C6CF", zorder=1)

    # plot data
    for i, yi in enumerate(y):
        ax.plot(x, yi)
        if shaded is not None:
            # NOTE: Lightening shaded area by adjusting alpha doesn't look great. Need
            # to update to reference a pre-set color pallete and keep alpha at fully
            # opaque.
            ax.fill_between(x, shaded[i][0], shaded[i][1], alpha=0.5)

    # set ax labels
    ax.set(xlabel=x_ax_label)
    ax.set(ylabel=y_ax_label)

    # set y-axis params
    setDefaultYAxisParams(ax, "left")

    # delete top, right, left spines
    makePatchSpinesInvisible(ax, ["top", "right", "left"])

    # pad left side of x-axis
    padXAxis(ax, "left")

    return fig


def fancy2YAxesPlot(
    x: ndarray,
    y: list[ndarray, ndarray],
    x_label: str,
    y_labels: list[str, str],
) -> Figure:
    """Plots two data sets with both y-axes on left side of figure.

    Args:
        x (`ndarray`): N-long 1-dimensional array.
        y (`list`[`ndarray`, `ndarray`]): Each array must be N-long and
            1-dimensional.
        x_label (`str`): x-axis label
        y_labels (`list`[`str`, `str`]): y axes labels

    Returns:
        Figure: A nice figure.
    """
    # create 2-axis figure
    fig = fancyLinePlot(x, y[0], x_ax_label=x_label, y_ax_label=y_labels[0])

    # get ax1
    ax1 = fig.get_axes()[0]
    # override line color
    # ax1.lines[0].set_color(colors_print_dict["blue2"])
    ax1.lines[0].set_color(color_map["print"]["blue2"])

    # create ax2
    ax2 = ax1.twinx()
    # plot and override line color
    # ax2.plot(x, y[1], color=colors_print_dict["burgundy"])
    ax2.plot(x, y[1], color=color_map["print"]["burgundy"])

    # delete ax2 spines
    makePatchSpinesInvisible(ax2)

    # set number of y-ticks in ax2 equal to ax1
    ax2.set_ylabel(y_labels[1])
    ax2.set_yticks(
        linspace(
            ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())
        )
    )

    # set ax1 colors and labels
    ax1.yaxis.label.set_color(ax1.lines[0].get_color())  # tick label color
    ax1.yaxis.set_tick_params(
        labelcolor=ax1.lines[0].get_color()
    )  # set tick color

    # set ax2 colors and labels
    setDefaultYAxisParams(ax2, "right")
    ax2.yaxis.label.set_color(ax2.lines[0].get_color())  # tick label color
    ax2.yaxis.set_tick_params(
        labelcolor=ax2.lines[0].get_color(), colors="#FFFFFF"
    )  # set tick color to transparent

    # scale ylimits to align yticks between ax2 and ax1
    pad1 = absolute(ax1.get_ylim()[0] - ax1.get_yticks()[1])
    pad1_norm = pad1 / absolute((ax1.get_yticks()[-2] - ax1.get_yticks()[1]))
    pad2 = pad1_norm * absolute((ax2.get_yticks()[-2] - ax2.get_yticks()[1]))
    ax2.set_ylim([ax2.get_yticks()[1] - pad2, ax2.get_yticks()[-2] + pad2])

    # overwrite pad x axis (only need to pad ax1 b/c ax2 is a twin of ax1)
    padXAxis(ax1, "both")

    return fig
