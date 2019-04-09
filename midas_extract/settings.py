# -*- coding: utf-8 -*-

"""Top-level package for midas-extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import datetime


DATA_DIR = os.environ.get('MIDAS_DATA_DIR', '/badc/ukmo-midas/data')
METADATA_DIR = os.environ.get('MIDAS_METADATA_DIR', '/badc/ukmo-midas/metadata')

if not os.path.isdir(DATA_DIR):
    raise Exception('Data directory does not exist: {}'.format(DATA_DIR))

if not os.path.isdir(METADATA_DIR):
    raise Exception('Metadata directory does not exist: {}'.format(METADATA_DIR))



def _now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M')

START_DEFAULT = '185901010000'
END_DEFAULT = _now()

