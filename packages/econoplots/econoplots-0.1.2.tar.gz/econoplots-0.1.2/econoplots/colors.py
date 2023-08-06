"""Run this script to generate color_map.json."""
# %% Imports
# Standard Library Imports
import json

# %% Colors and parameters
colors_web_dict = {
    "econ_red": "#E3120B",
    "black": "#0C0C0C",
    "boxes_nav": ["#E9EDF0", "#B7C6CF", "#758D99"],
    "text": "#3F5661",
    "red": "#DB444B",
    "blue": "#006BA2",
    "cyan": "#3EBCD2",
    "green": "#379A8B",
    "yellow": "#EBB434",
    "olive": "#B4BA39",
    "purple": "#9A607F",
    "gold": "#D1B07C",
    "grey": "#758D99",
    "grey1": "#758D99",
    "grey2": "#3F5661",
    "grey3": "#6F8793",
    "grey4": "#89A2AE",
    "grey5": "#A4BDC9",
    "grey6": "#BFD8E5",
}

colors_print_dict = {
    "econ_red": (238, 28, 27),
    "red1": (221, 110, 110),
    "red_text": (216, 88, 92),
    "blue1": (18, 111, 162),
    "blue2": (43, 192, 210),
    "blue2_text": (0, 171, 196),
    "gold": (224, 178, 102),
    "burgundy": (151, 60, 77),
    "tan": (171, 139, 149),
    "dark_teal": (0, 151, 159),
    "cyan": (113, 202, 199),
}

main_keys = [
    "red",
    "blue",
    "cyan",
    "green",
    "yellow",
    "olive",
    "purple",
    "gold",
    "grey",
]

grid_color = {"grid_gray": "#B7C6CF"}


# %% Save color references as JSON
def _normalizeRGBdict(rgb_dict):
    for key, val in zip(rgb_dict.keys(), rgb_dict.values()):
        val = _normalizeRGB([val])
        rgb_dict[key] = val[0]
    return rgb_dict


def _normalizeRGB(list_of_tuples):
    new_colors = [() for x in list_of_tuples]
    for i, col in enumerate(list_of_tuples):
        new_colors[i] = [element / 256 for element in col]

    return new_colors


if __name__ == "__main__":
    # Run to save color map JSON file.
    colors_print_dict = _normalizeRGBdict(colors_print_dict)

    cm_web_main = [colors_web_dict.get(key) for key in main_keys]

    line_chart_keys = ["blue1", "blue2", "gold", "burgundy", "dark_teal", "tan"]
    cm_line_chart = [colors_print_dict.get(key) for key in line_chart_keys]

    grey_keys = ["grey" + str(x) for x in range(1, 7)]
    colors_greys = [colors_web_dict.get(key) for key in grey_keys]

    color_map_master = {
        "print": colors_print_dict,
        "web": cm_web_main,
        "line_chart": cm_line_chart,
        "greys": colors_greys,
        "grid": grid_color,
    }

    json_obj = json.dumps(color_map_master)
    with open("econoplots/color_map.json", "w") as outfile:
        outfile.write(json_obj)
