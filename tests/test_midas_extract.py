#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `midas_extract` package."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.1.0"


import pytest
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
    'filter': (
        ['--table', 'TD', '--start', '', '--end', '2017091011000'],
        ['--table', 'TD', '--start', '201709010000', '--end', '201802011000', '--output_filepath', '/tmp/outputfile.dat'],
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
         

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    pass


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


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


def test_cli_get_stations_successes():
    """Test multiple successful get_stations call via the CLI."""
    runner = CliRunner()

    sub_cmd = 'stations' 
    # Test all successes
    for inputs in _INPUTS[sub_cmd]:

        result = runner.invoke(cli.main, [sub_cmd] + inputs)
        assert result.exit_code == 0


def test_get_stations_successes():
    """Test multiple successful get_stations call in python."""
    # Test all successes
    for inputs in _INPUTS['stations']:

        kwargs = _map_inputs(inputs)
        result = cli.get_stations(**kwargs)


def test_cli_filter_records_fail():
    """Test a failed filter call via the CLI."""
    runner = CliRunner()

    # Test a failure
    result = runner.invoke(cli.main, 'filter')
    assert result.exit_code == 1
    assert 'Error: Must provide table ID with "-t" argument.' in result.output


def test_cli_filter_records_successes():
    """Test multiple successful get_stations call via the CLI."""
    runner = CliRunner()

    sub_cmd = 'stations'
    # Test all successes
    for inputs in _INPUTS[sub_cmd]:

        result = runner.invoke(cli.main, [sub_cmd] + inputs)
        assert result.exit_code == 0


def test_filter_records_successes():
    """Test multiple successful get_stations call in python."""
    # Test all successes
    for inputs in _INPUTS['stations']:

        kwargs = _map_inputs(inputs)
        result = cli.get_stations(**kwargs)

