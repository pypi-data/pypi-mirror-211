"""
This file contains methods that are related to python's defaultdict object
from the collections package.
"""

from collections import defaultdict
from typing import Type
import numpy as np


def nested_ddict(depth: int, endtype: Type):
    """
    Creates defaultdict that is arbitrarily nested. For example,
    if we write `d = nested_ddict(3, list)` then we can do something
    like `d['0']['1']['2']['3'].append('stuff')`.

    Parameters:
    depth - How deep the defaultdict is
    endtype - What type the value of the deepest default dict is.
    """
    if depth == 0:
        return defaultdict(endtype)
    return defaultdict(lambda: nested_ddict(depth - 1, endtype))


def format_ddict(ddict: defaultdict, make_nparr: bool = True, sort_lists: bool = False):
    """
    Turn nested defaultdicts into nested dicts and,optionally lists in numpy arrays.

    Parameters:
    ddict - Defaultdict to transform
    make_nparr - If True, will turn lists into numpy arrays
    sort_list - If True, will sort any lists it finds
    """
    if isinstance(ddict, (dict, defaultdict)):
        ddict = {k: format_ddict(v, sort_lists) for k, v in ddict.items()}
    elif isinstance(ddict, list):
        ddict = sorted(ddict) if sort_lists else ddict
        ddict = np.array(ddict) if make_nparr else ddict
    return ddict
