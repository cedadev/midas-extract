# -*- coding: utf-8 -*-

"""Tests for `midas_extract` package."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.1.0"

import os
import shutil
import pytest
from pathlib import Path
from queue import deque

from click.testing import CliRunner

from midas_extract import cli


_INPUTS = {
    'stations': (
        ['--county', 'cornwall,devon,wiltshire'],
        ['--bbox', '54,0,52,3'],
        ['--bbox', '54,0,52,3', '--quiet'],
        ['--bbox', '52,0.2,51,0.4', '--start', '200301010000'],
        ['--bbox', '52,0.2,51,0.4', '--start', '200301010000', '--data-type', 'rain'],
        ['--county', 'cornwall', '--start', '199901010000', '--end', '200501010000', '--data-type', 'rain'],
        ['--county', 'DEVON', '--start', '199901010000', '--end', '200501010000', '--data-type', 'rain'],
        ['--county', 'DEVON', '--end', '200501010000', '--data-type', 'rain'],
        ['--county', 'DEVON', '--end', '200501010000', '--data-type', 'rain', '--output-filepath', '/tmp/stations.txt'],
    ),
    'extract': (
        ['--table', 'TD', '--start', '', '--end', '2017091011000'],
        ['--table', 'TD', '--start', '201709010000', '--end', '201802011000', '--output-filepath', '/tmp/outputfile.dat'],
        ['--table', 'TD', '--start', '200401010000', '--end', '200401011000', '--src-ids', '214,926', '--delimiter', 'tab'],
    )
}


def _fix_key(key):
    return key.lstrip('-').replace('-', '_') 


def _map_inputs(inputs_list):
    """Maps a list of inputs to a dictionary of kwargs."""
    inputs = {}
    d = deque(inputs_list)

    while d:
  
        key = d.popleft()
        key = _fix_key(key)

        if (d and d[0].startswith('--')) or not d:
            value = True
        else:
            value = d.popleft()

        inputs[key] = value

    return inputs
         


def test_cli_help():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Returns a list of stations SRC IDs based on inputs.' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_cli_get_stations_fail():
    """Test a failed get_stations call via the CLI."""
    runner = CliRunner()

    # Test a failure
    result = runner.invoke(cli.main, 'stations')
    assert result.exit_code == 1
    assert 'Error: You must provide a miminum of either a list of counties or bbox coordinates.' in result.output


def test_1(midas_metadata):
    runner = CliRunner()
    sub_cmd = 'stations'

    # Test all successes
    result = runner.invoke(cli.main, [sub_cmd] + _INPUTS['stations'][0])
    assert result.exit_code == 0



@pytest.mark.parametrize('inputs', _INPUTS['stations'])
def test_cli_get_stations_successes(midas_metadata, inputs):
    """Test multiple successful get_stations call via the CLI."""
    runner = CliRunner()
    sub_cmd = 'stations' 

    # Test all successes
    result = runner.invoke(cli.main, [sub_cmd] + inputs)
    assert result.exit_code == 0


@pytest.mark.parametrize('inputs', _INPUTS['stations'])
def test_get_stations_successes(midas_metadata, inputs):
    """Test multiple successful get_stations call in python."""
    # Test all successes
    kwargs = _map_inputs(inputs)
    result = cli.get_stations(**kwargs)


def test_cli_extract_records_fail(midas_metadata, midas_data):
    """Test a failed extract call via the CLI."""
    runner = CliRunner()

    # Test a failure
    result = runner.invoke(cli.main, 'extract')
    assert result.exit_code == 1
    assert 'Error: Must provide table ID with "-t" argument.' in result.output


def test_cli_extract_2(midas_metadata, midas_data):
    runner = CliRunner()
    sub_cmd = 'extract'

    # Test all successes
    result = runner.invoke(cli.main, [sub_cmd] + _INPUTS['extract'][0])
    assert result.exit_code == 0


@pytest.mark.parametrize('inputs', _INPUTS['extract'])
def test_cli_extract_records_successes(midas_metadata, midas_data, inputs):
    """Test multiple successful get_stations call via the CLI."""
    runner = CliRunner()
    sub_cmd = 'extract'

    # Test all successes
    result = runner.invoke(cli.main, [sub_cmd] + inputs)
    assert result.exit_code == 0


@pytest.mark.parametrize('inputs', _INPUTS['extract'])
def test_extract_records_successes(midas_metadata, midas_data, inputs):
    """Test multiple successful get_stations call in python."""
    # Test all successes
    kwargs = _map_inputs(inputs)
    result = cli.extract_records(**kwargs)


