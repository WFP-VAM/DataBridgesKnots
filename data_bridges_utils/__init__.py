# encoding: utf-8

"""
Wrapper for DataBridges client.
"""
import stata_setup

from .get_data import DataBridgesShapes

try:
    stata_setup.config('C:/Program Files/Stata18', 'se')
except OSError:
    pass

__all__ = ['DataBridgesShapes', 'load_stata']
