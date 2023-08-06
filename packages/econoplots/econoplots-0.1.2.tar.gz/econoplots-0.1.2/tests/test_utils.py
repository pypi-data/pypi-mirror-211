"""Test utils."""
# %% Imports
# Third Party Imports
from matplotlib import pyplot as plt

# econoplots Imports
from econoplots.params import setRCParams
from econoplots.utils import replaceAxesMinusGlyphs, replaceMinusWithHyphen

# %% Set params
setRCParams()
# %% Test replace minus signs

fig, axs = plt.subplots(2)
axs[0].axis([-4, 4, -4, 4])
axs[1].axis([-4, 4, -4, 4])
axs[0].text(-3, 2, "Unreplaced tick labels")
axs[1].text(-3, 2, "Replaced tick labels")
axs[0].text(0, 2, "- Hyphen")
axs[0].text(0, 0, chr(8722) + " Minus sign (unreplaced)")
more_text = axs[0].text(0, -2, chr(8722) + " Minus sign (replaced)")
# ax = fig.axes[0].xaxis

new_text = replaceMinusWithHyphen(more_text)
replaceAxesMinusGlyphs(axs[1])

plt.show()
