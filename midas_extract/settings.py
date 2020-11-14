# -*- coding: utf-8 -*-

"""Top-level package for midas-extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import datetime


def _now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M')

START_DEFAULT = '185901010000'
END_DEFAULT = _now()


def get_data_dir():
    data_dir = os.environ.get('MIDAS_DATA_DIR', '/badc/ukmo-midas/data')

    if not os.path.isdir(data_dir):
        raise Exception(f'Data directory does not exist: {data_dir}')

    return data_dir


def get_metadata_dir():
    metadata_dir = os.environ.get('MIDAS_METADATA_DIR', '/badc/ukmo-midas/metadata')

    if not os.path.isdir(metadata_dir):
        raise Exception(f'Metadata directory does not exist: {metadata_dir}')

    return metadata_dir

