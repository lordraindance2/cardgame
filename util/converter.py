import re
import numpy as np


def convert(string: str) -> list:
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.strip()
    if string is None or string is "":
        return [-1]

    a = string.split(",")
    return [int(s) for s in a]


def escape_underscore(string: str) -> str:
    return string.replace("_", "\_")
