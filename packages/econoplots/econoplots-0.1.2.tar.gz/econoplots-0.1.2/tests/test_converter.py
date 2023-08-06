"""Tests for converter.py."""
# %% Imports
# Standard Library Imports
from copy import deepcopy

# Third Party Imports
from matplotlib import pyplot as plt
from numpy import arange, array, cos, max, min, sin

# Econoplots Imports
from econoplots.converter import convert2Econo

# %% Make data
x = arange(-1, 1, 0.1)
y = array([1 * sin(x), 2 * cos(x)]).T
print(f"min(x) = {min(x)}")
print(f"max(x) = {max(x)}")
print(f"min(y) = {min(y)}")
print(f"max(y) = {max(y)}")

fig, ax = plt.subplots()
ax.plot(x, y, color="red")
ax.set_xlabel("X label here")
ax.set_ylabel("Y label here")

# %% Test converter function
ax_new = convert2Econo(deepcopy(ax))
# %% done
plt.show()
print("done")
