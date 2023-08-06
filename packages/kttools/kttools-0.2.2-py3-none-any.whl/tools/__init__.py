#!/usr/bin/env python
# @Author: Kelvin
# @Date:   2022-07-18 11:09:04
# @Last Modified by:   Kelvin
# @Last Modified time: 2022-07-18 11:55:02
"""tools package"""
import matplotlib

FONTTYPE = 42

# set the font so no weird lines and boxes are made during export
matplotlib.rcParams["pdf.fonttype"] = FONTTYPE
matplotlib.rcParams["ps.fonttype"] = FONTTYPE


# import sub-modules
from .sc import *
from .tools import *

__all__ = sc.__all__ + tools.__all__
