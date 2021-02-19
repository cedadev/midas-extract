# -*- coding: utf-8 -*-

"""Tests for components of `midas_extract.subsetter`."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.1.0"

from midas_extract.subsetter import pad_time


def test_pad_time():
    args = [
        ['0001', ('000101010000', '000112312359')],
        ['9999', ('999901010000', '999912312359')],
        ['202002', ('202002010000', '202002312359')],
        ['19421130', ('194211300000', '194211302359')],
        ['1859041223', ('185904122300', '185904122359')],
        ['000101010001', ('000101010001', '000101010001')],
    ]

    for ts, (start, end) in args:
        assert(pad_time(ts, "start") == start)
        assert(pad_time(ts, "end") == end)
