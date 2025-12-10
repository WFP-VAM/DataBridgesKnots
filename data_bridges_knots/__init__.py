# encoding: utf-8

"""
Wrapper for DataBridges client.
"""

from .client import DataBridgesShapes
from .labels import (get_variable_labels, get_value_labels, map_value_labels)

__all__ = [
    "DataBridgesShapes",
    "labels",
    "get_variable_labels",
    "get_value_labels",
    "map_value_labels",
]
