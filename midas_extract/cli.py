# -*- coding: utf-8 -*-

"""Console script for midas_extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import sys
import click
import tempfile

from midas_extract.settings import START_DEFAULT, END_DEFAULT
from midas_extract.stations import StationIDGetter
from midas_extract.subsetter import MIDASSubsetter


@click.group()
def main():
   pass


@main.command('extract')
@click.option('--output-filepath', '-o', default=None, help='Output file path (optional)')
@click.option('--table', '-t', default=None, help='MIDAS Database table identifier')
@click.option('--start', '-s', default=None, help='Start datetime as: YYYYMMDDhhmm')
@click.option('--end', '-e', default=None, help='End datetime as: YYYYMMDDhhmm')
@click.option('--columns', '-c', default='all', help='Columns to keep in the output')
@click.option('--conditions', '-n', default=None, help='Conditions with which to extract data')
@click.option('--src-ids', '-i', default=None, help='Comma-separated list of station SRC IDs')
@click.option('--delimiter', '-d', default='default', help='Delimiter for output files')
@click.option('--region', '-r', default=None, help='Region')
@click.option('--src-id-file', '-f', default=None, help='File containing a list of SRC IDs')
@click.option('--tmp-dir', '-p', default=None, help='Path to temporary directory')
def extract(output_filepath=None, table=None, start=None, end=None, columns='all',
           conditions=None, src_ids=None, delimiter='default', region=None, src_id_file=None,
           tmp_dir=None):
    """
    Filters records in a MIDAS data table (across multiple files).

    Available extracts:
      - table
      - datetime
      - columns
      - conditions
      - station SRC IDs
      - region 

    The output can be modified by delimiter. 

    Subsets a MIDAS data table (across multiple files).
    """
    return extract_records(**vars())


def extract_records(output_filepath=None, table=None, start=None, end=None, columns='all',
           conditions=None, src_ids=None, delimiter='default', region=None, src_id_file=None,
           tmp_dir=None):
    """ 
    Subsets data from the MIDAS flat files. Allows extraction by:

    The MIDASSubsetter class needs to be able to see the file 'midas_structure.txt' which
    is essentially a description of the table contents in a text file. This is parsed each
    time this script is called.

    There is hard-coded limit of 100,000 lines that can currently be extracted.

Where:
------

    <table>     - is the name of the MIDAS table
    -s          - provide the start date/time
    -e          - provide the end date/time
    -c          - provide a comma-separated list of required columns
    -n          - provide a list of comma-separated list of conditions in the form:
                    * range=<low>:<high>     [<low> and <high> are values]
                    * greater_than=<value>
                    * less_than=<value>
                    * exact=<match>          [<match> is a string]
                    * pattern=<pattern>      [<pattern> is a regular expression]
    -d          - delimiter is one of ","|"comma"|"tab" or other character/string.
    -i          - provide a comma separated list of station IDs
    -g          - provide the name of a file containing one station id per line.
    -r          - for GLOBAL table only - provide a region (optional - otherwise will do global search).
                  Regions are: 1-Africa, 2-Asia, 3-South America, 4-North Central America,
                               5-South West Pacific, 6-Europe, 7-Antarctic.
    -p           - temporary directory location (absolute path)

Examples:
=========

    midas_extract extract -t RS -s 200401010000 -e 200401011000
    midas_extract extract -t RS -s 200401010000 -e 200401011000 outputfile.dat
    midas_extract extract -t RS -s 200401010000 -e 200401011000 -g testlist.txt outputfile.dat
    midas_extract extract -t RS -s 200401010000 -e 200401011000 -i 214,926 -d tab

    """
    if not output_filepath:
        output_filepath = 'display'

    if conditions:
        conditions = {}
        condition_list = value.split(',')

        for cond in condition_list:
            a, b = cond.split('=')
            conditions[a] = b 

    if src_ids:
        src_ids = src_ids.strip('.')

    if not tmp_dir:
        tmp_dir = tempfile.gettempdir()

    if src_id_file:
        src_ids = open(src_id_file).read().strip().split()

    if not table:
        raise click.ClickException('Must provide table ID with "-t" argument.')

    return MIDASSubsetter(table, output_filepath, start, end, columns, conditions,
                          src_ids, region, delimiter, tmp_dir=tmp_dir)


@main.command('stations')
@click.option('--output-filepath', '-o', default=None, help='Output file path (optional)')
@click.option('--county', '-c', default=None, help='Comma-separated county list')
@click.option('--bbox', '-b', default=None, help='Bounding box as: N,W,S,E')
@click.option('--quiet', '-q', is_flag=True, help='Print all output to terminal')
@click.option('--counties-file', '-f', default=None, help='Location of counties file, one per line')
@click.option('--start', '-s', default=None, help='Start datetime as: YYYYMMDDhhmm')
@click.option('--end', '-e', default=None, help='End datetime as: YYYYMMDDhhmm') 
@click.option('--data-type', '-d', default=None, help='List of data types')
def stations(output_filepath=None, county=None, bbox=None, quiet=False, counties_file=None,
                 start=None, end=None, data_type=None):
    """
    Returns a list of stations SRC IDs based on inputs.
    """
    return get_stations(**vars())


def get_stations(output_filepath=None, county=None, bbox=None, quiet=False, counties_file=None,
                 start=None, end=None, data_type=None):
    """
    Returns a list of stations SRC IDs based on inputs.
    """
    if not county:
        county = []
    else:
        county = county.split(',')

    if bbox:
        bbox = bbox.split(',')

    if counties_file:
        with open(counties_file) as reader:
            county = reader.read().strip().split()

    if start:
        start = int(start)
    if end:
        end = int(end)

    if not data_type:
        data_type = []
    else:
        data_type = data_type.split(',')

    if not county and not bbox:
        raise click.ClickException("You must provide a miminum of either a list of counties or " \
                                   "bbox coordinates.")

    return StationIDGetter(county, bbox, start_time=start, end_time=end, data_type=data_type,
                           output_file=output_filepath, quiet=quiet)


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
