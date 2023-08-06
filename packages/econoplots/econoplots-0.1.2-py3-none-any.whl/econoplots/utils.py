"""Utilities."""
# Imports
from __future__ import annotations

# Standard Library Imports
import importlib.resources
import json
from itertools import cycle
from typing import Tuple

# Third Party Imports
from matplotlib import pyplot as plt  # noqa
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.text import Text
from matplotlib.ticker import AutoMinorLocator, FixedLocator
from numpy import absolute, append, intersect1d

# %% Functions


def loadColorMap() -> dict:
    with importlib.resources.open_text("econoplots", "color_map.json") as file:
        color_map = json.load(file)
    return color_map


def makePatchSpinesInvisible(
    ax: Axis,
    list_of_spines: list[str] = None,
) -> None:
    """Makes spine(s) of axis invisible.

    Args:
        ax (Axis): A matplotlib Axis
        list_of_spines (list[str], optional): Entries can be any
            combination of 'top', 'bottom', 'left', or 'right'. Spines in ax
            associated with list_of_spines will be made invisible. If None,
            then all spines will be made invisible. Defaults to None.
    """
    if list_of_spines is None:
        list_of_spines = ["top", "bottom", "left", "right"]
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in list_of_spines:
        ax.spines[sp].set_visible(False)

    return


def replaceAxesMinusGlyphs(ax: Axes) -> None:
    """Replace x- and y-axes minus signs with hyphens."""
    x_labels = []
    tick_labels = ax.xaxis.get_ticklabels()
    for tl in tick_labels:
        x_labels.append(replaceMinusWithHyphen(tl))
    ax.xaxis.set_ticklabels(x_labels)

    y_labels = []
    tick_labels = ax.yaxis.get_ticklabels()
    for tl in tick_labels:
        y_labels.append(replaceMinusWithHyphen(tl))
    # ax.yaxis.set_ticklabels(y_labels)
    ytick_locs = ax.yaxis.get_ticklocs()
    ax.set_yticks(ytick_locs[1:-2], y_labels[1:-2])

    return


def setDefaultYAxisParams(
    ax: Axes,
    side: str,
    label_location: str,
) -> None:
    """Set y-axis side, label, tick label location and style.

    Args:
        ax (Axes): _description_
        side (str): "left" or "right
    """
    color_map = loadColorMap()

    # Set axis parameters based on which side axis is on
    if side == "right":
        ha = "right"
        label_side = {
            "labelright": True,
            "labelleft": False,
        }
        left_right_pad = -2
    elif side == "left":
        ha = "left"
        label_side = {
            "labelleft": True,
            "labelright": False,
        }
        left_right_pad = -2

    # Set tick parameters
    ax.yaxis.set_tick_params(
        pad=left_right_pad,  # Pad tick labels so they don't go over y-axis
        colors=color_map["grid"]["grid_gray"],  # set tick color to same as grid
        labelcolor="black",  # set tick label color
        **label_side,
    )

    # ax.ticklabel_format(ScalarFormatter)

    # Set tick label parameters
    # NOTE: Move labels after moving axis.
    # set vertical alignment on y-axis tick labels to be on top of of major
    # ticks. Set horizontal alignment to right (this part not necessary)
    for label in ax.yaxis.get_ticklabels():
        label.set_verticalalignment("bottom")
        label.set_horizontalalignment(ha)

    # Move yaxis label to upper-left or -right
    relocateYAxisLabel(ax, side=label_location)

    return


def setDefaultXAxisParams(
    ax: Axes,
    pad_side: str,
    minor_ticks_on: bool = True,
    n_minortick_subdivisions: int = None,
):
    """Set x-axis padding, label, tick label location and style.

    Args:
        ax (Axes): _description_
        pad_side (str): Which side(s) to add padding to. Axis is always shown on
            bottom of plot.
        minor_ticks_on (bool, optional): Whether or not to plot minor tick marks.
            Defaults to True.
        n_minortick_subdivisions (int, optional): Number of minor ticks between
            major ticks. Defaults to None, which automatically determines number.
    """
    # Add empty space to x-axis to give space between y-tick labels and plotted
    # data. Do this BEFORE other operations, as resizing can mess up tick marks.
    padXAxis(ax, side=pad_side)

    # Set Major ticks. Make major ticks that are wider than span of the data invisible.
    makeOutOfRangeXTicksInvisible(ax)

    if minor_ticks_on is True:
        # Turn on minor ticks and set frequency between major ticks
        addInnerMinorTicks(ax, n_minortick_subdivisions)

    # Add minor tick(s) if outer limits of data are NOT on major ticks. Unlike
    # minor ticks that are in-between major ticks, the outer minor ticks are not
    # optional.
    addOuterMinorTicks(ax)

    return


def addInnerMinorTicks(ax: Axes, n_minortick_subdivisions: int | None):
    """Add minor ticks to x axis within data limits."""
    ax.xaxis.set_minor_locator(AutoMinorLocator(n_minortick_subdivisions))

    # Remove minor ticks that are beyond data range.
    x_lims, _ = getDataLimits(ax)
    # min_major_tick_loc = ax.xaxis.get_majorticklocs()[1]
    # max_major_tick_loc = ax.xaxis.get_majorticklocs()[-2]
    minor_tick_locs = ax.xaxis.get_minorticklocs()
    minor_tick_locs = minor_tick_locs[minor_tick_locs > x_lims[0]]
    minor_tick_locs = minor_tick_locs[minor_tick_locs < x_lims[1]]
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))
    return


def makeOutOfRangeXTicksInvisible(ax: Axes):
    """Make major ticks that are < or > data range invisible."""
    major_tick_locs = ax.xaxis.get_majorticklocs()
    xticks = ax.xaxis.get_major_ticks()
    xlims, _ = getDataLimits(ax)
    visibility = list(major_tick_locs > xlims[0])

    for tick, vis in zip(xticks, visibility):
        tick.set_visible(vis)
    visibility = list(major_tick_locs < xlims[1])
    for tick, vis in zip(xticks, visibility):
        tick.set_visible(vis)

    return


def addOuterMinorTicks(ax: Axes):
    """Add minor ticks to data limits if major ticks don't already cover limits."""
    major_locs = [b.get_loc() for b in ax.xaxis.get_major_ticks()]
    minor_tick_locs = ax.xaxis.get_minorticklocs()

    # Get locations to add new minor ticks. Add new ticks if existing major ticks
    # don't overlap with outer limits of data.
    x_lim, _ = getDataLimits(ax)
    new_locs = []
    for x in x_lim:
        if x not in major_locs:
            new_locs.append(x)
    num_new_locs = len(new_locs)

    # Append new minor ticks to existing minor ticks.
    minor_tick_locs = append(minor_tick_locs, new_locs)
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))

    # Refresh minor tick locs because special case where adding minor tick close
    # to major tick causes minor tick to not be added. This step is needed to prevent
    # an error.
    num_minor_ticks_attempted = len(minor_tick_locs)
    minor_tick_locs = ax.xaxis.get_minorticklocs()
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))

    if num_minor_ticks_attempted != len(minor_tick_locs):
        # Par down the list of new minor tick locations if matplotlib rejected
        # additions.
        print("Different number of minor ticks added than attempted.")
        new_locs = intersect1d(minor_tick_locs, new_locs)
        num_new_locs = len(new_locs)

    # Create labels for new minor ticks and set minor tick labels
    minor_labels = [item.get_text() for item in ax.get_xticklabels(minor=True)]
    num_minor_labels = len(minor_labels)
    for i, lab in enumerate(new_locs, num_minor_labels - num_new_locs):
        # new labels are at end of minor_labels list
        text = "%.0f" % lab
        minor_labels[i] = text

    # TODO: Make the format of the added minor ticks match the format of the major
    # ticks.
    ax.set_xticks(minor_tick_locs, minor_labels, minor=True)

    return


def padXAxis(
    ax: Axes,
    side: str,
) -> Axes:
    """Add extra space on both sides of the x-axis.

    Adds 15% padding on the input side, and 5% padding on the opposite side. If
    "both" sides are selected, adds 15% padding to both sides.

    Args:
        ax (Axes): _description_
        side (str): "left" | "right" | "both"

    Returns:
        Axes: _description_
    """
    # Get real bounds of x-axis data (not x-axis limits, which are wider than data)
    x_lims, _ = getDataLimits(ax)

    # get axis pad amount
    x_ax_pad = 0.15 * absolute(x_lims[1] - x_lims[0])
    x_ax_minor_pad = 0.33 * x_ax_pad

    if side == "left":
        # set x-axis max limit to tighter than default and with extra room on left
        ax.set_xlim(
            [
                x_lims[0] - x_ax_pad,
                x_lims[1] + x_ax_minor_pad,
            ]
        )

    if side == "right":
        ax.set_xlim(
            [
                x_lims[0] - x_ax_minor_pad,
                x_lims[1] + x_ax_pad,
            ]
        )

    if side == "both":
        ax.set_xlim(
            [
                x_lims[0] - x_ax_pad,
                x_lims[1] + x_ax_pad,
            ]
        )

    # NOTE: This adjustment seems to have not been necessary, but keeping here
    # in case issue crops up again.
    # Changing plot size changes tick labels in incorrect ways, so re-initialize
    # tick labels
    # ax.set_xticks(ax.xaxis.get_majorticklocs()[1:-2])

    return ax


def getDataLimits(ax: Axes) -> Tuple[list, list]:
    """Get x and y limits of data in ax (different from axis limits).

    Args:
        ax (Axes): _description_

    Returns:
        x_lims(list): x data limits [min, max]
        y_lims(list): y data limits [min, max]
    """
    x_lims = [0, 0]
    y_lims = [0, 0]
    for line in ax.lines:
        xdat = line.get_xdata()
        ydat = line.get_ydata()
        min_x = xdat.min()
        max_x = xdat.max()
        min_y = ydat.min()
        max_y = ydat.max()

        if min_x < x_lims[0]:
            x_lims[0] = min_x
        if max_x > x_lims[1]:
            x_lims[1] = max_x

        if min_y < y_lims[0]:
            y_lims[0] = min_y
        if max_y > y_lims[1]:
            y_lims[1] = max_y

    return x_lims, y_lims


def setDefaultLineColors(ax: Axes) -> Axes:
    """Sets colors of all lines in ax to default line chart colors.

    Args:
        ax (Axes): _description_

    Returns:
        Axes: _description_
    """
    color_map = loadColorMap()
    color_cycler = cycle(color_map["line_chart"])
    for line in ax.lines:
        line.set_color(next(color_cycler))

    return ax


def relocateYAxisLabel(ax: Axes, side: str) -> Axes:
    """Move y-axis label to top of plot.

    Args:
        ax (Axes): _description_
        side (str): "left" or "right"

    Returns:
        Axes: _description_
    """
    ax.yaxis.label.set(rotation="horizontal")

    # Set label vertical alignment
    ax.yaxis.label.set_va("bottom")

    # TODO: Get max value of yticklabel, then place yaxis label above that. Will
    # be smarter than simply placing the yaxis label at an arbitrary location.
    ytick_labels = ax.yaxis.get_majorticklabels()
    ytick_label_locs = [label.get_position()[1] for label in ytick_labels]
    # get max visible ytick label location
    top_label_loc = ytick_label_locs[-2]

    # Add a bit of white space between the bottom of the label and the top of the
    # axis.
    # y_label_pad = 0
    y_label_pad = 0.01
    # y_label_pad = 0.05

    if side == "left":
        # move label to upper-left and set horizontal alignment
        ax.yaxis.set_label_coords(0, 1 + y_label_pad)
        ax.yaxis.label.set_ha("left")
    elif side == "right":
        # move label to upper-right and set horizontal alignment
        ax.yaxis.set_label_coords(1, 1 + y_label_pad)
        ax.yaxis.label.set_ha("right")

    return ax


def replaceMinusWithHyphen(text: Text) -> Text:
    """Replace all minus signs chr(8722) with hyphens chr(45)."""
    t = text._text
    text._text = t.replace(chr(8722), "-")
    return text
