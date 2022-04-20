import os

CARTED_SIGN = "*"

COLOR = {
    "normal": (7, 0),
    "selected": (0, 7),
    "dir": (12, 0),
    "dirSelected": (0, 12),
    "dimmed": (8, 0),
    "dirDimmed": (4, 0),
    "pathStr": (8, 0),
    "pathStrSelected": (0, 7),
    "fill": (0, 0),
    "fillSelected": (0, 4),
    "line": (8, 0),
    "lineSelected": (7, 0),
    "carted": (15, 0),
    "confirm": (7, 0),
    "confirmSelected": (0, 7),
}


if "256" in os.environ.get("TERM", ""):
    COLOR = {
        "normal": (7, 0),
        "selected": (0, 7),
        "dir": (12, 0),
        "dirSelected": (0, 12),
        "dimmed": (8, 0),
        "dirDimmed": (4, 0),
        "pathStr": (8, 0),
        "pathStrSelected": (0, 7),
        "fill": (0, 0),
        "fillSelected": (0, 4),
        "line": (8, 0),
        "lineSelected": (7, 0),
        "carted": (15, 0),
        "confirm": (7, 0),
        "confirmSelected": (0, 15),
    }
