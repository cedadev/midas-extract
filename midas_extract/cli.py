# -*- coding: utf-8 -*-

"""Console script for midas_extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import sys
import click

from midas_extract.settings import START_DEFAULT, END_DEFAULT
from midas_extract.stations import StationIDGetter


@click.group()
def main():
   pass


@main.command()
@click.option('--output-filepath', '-o', default=None, help='Output file path (optional)')
@click.option('--tables', '-t', default=None, help='Comma-separated list of database tables')
@click.option('--start', '-s', default=None, help='Start datetime as: YYYYMMDDhhmm')
@click.option('--end', '-e', default=None, help='End datetime as: YYYYMMDDhhmm')
@click.option('--columns', '-c', default='all', help='Columns to keep in the output')
@click.option('--conditions', '-n', default=None, help='Conditions with which to filter data')
@click.option('--src-ids', '-i', default=None, help='Comma-separated list of station SRC IDs')
@click.option('--delimiter', '-d', default='default', help='Delimiter for output files')
@click.option('--region', '-r', default=None, help='Region')
@click.option('--src-id-file', '-f', default=None, help='File containing a list of SRC IDs')
@click.option('--tempdir', '-p', default=None, help='Path to temporary directory')
def subset(output_filepath=None, tables=None, start=None, end=None, columns='all',
           conditions=None, src_ids=None, delimiter='default', region=None, src_id_file=None,
           tempdir=None):

    if not output_filepath:
        output_filepath = 'display'

    if start:
        start = long(start)
    if end:
        end = long(end)

    if conditions:
        conditions = {}
        condition_list = value.split(',')

        for cond in condition_list:
            a, b = cond.split('=')
            conditions[a] = b 

    if src_ids:
        src_ids = src_ids.strip('.')

    if not temp_dir:
        temp_dir = _get_temp_dir()

    if src_id_file:
        src_ids = open(src_id_file).read().strip().split()

    if not tables:
        click.ClickException('Must provide table name(s) with "-t" argument.')

    return MIDASSubsetter(tables, output_filepath, start, end, columns, conditions,
                          src_ids, region, delimiter, temp_dir=temp_dir)


"""
midasSubsetter.py
=================

Subsets data from the MIDAS flat files. Allows extraction by:

- table
- date range
- column name
- value conditions

The MIDASSubsetter class needs to be able to see the file 'midas_structure.txt' which
is essentially a description of the table contents in a text file. This is parsed each
time this script is called.

There is hard-coded limit of 100,000 lines that can currently be extracted.

Usage:
======

    midas_extract subsetter -t <table> [-s <YYYYMMDDhhmm>] [-e <YYYYMMDDhhmm>]
         [-c <column1>[,<column2>...]] [-n <conditions>] [-d <delimiter>]
         [-i <src_id1>[,<src_id2>...]] [-g <groupfile>] [-r <region>] [-p <tempdir>] <outputFile>


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

    midas_extract subsetter -t RS -s 200401010000 -e 200401011000
    midas_extract subsetter -t RS -s 200401010000 -e 200401011000 outputfile.dat
    midas_extract subsetter -t RS -s 200401010000 -e 200401011000 -g testlist.txt outputfile.dat
    midas_extract subsetter -t RS -s 200401010000 -e 200401011000 -i 214,926 -d tab
"""


@main.command()
@click.option('--output-filepath', '-o', default=None, help='Output file path (optional)')
@click.option('--county', '-c', default=None, help='Comma-separated county list')
@click.option('--bbox', '-b', default=None, help='Bounding box as: N,W,S,E')
@click.option('--quiet', '-q', is_flag=True, help='Print all output to terminal')
@click.option('--counties-file', '-f', default=None, help='Location of counties file, one per line')
@click.option('--start', '-s', default=None, help='Start datetime as: YYYYMMDDhhmm')
@click.option('--end', '-e', default=None, help='End datetime as: YYYYMMDDhhmm') 
@click.option('--data-type', '-d', default=None, help='List of data types')
def get_stations(output_filepath=None, county=None, bbox=None, quiet=False, counties_file=None,
                 start=None, end=None, data_type=None):
    """
    Takes a county or list of counties and returns a list of station IDs (src_id).

    midas_extract get_stations  -c cornwall,devon,wiltshire
    midas_extract get_stations  -b 52,54,0,3
    midas_extract get_stations  -b 52,54,0,3 -n
    midas_extract get_stations  -b 52,52.2,0.2,0.4 -s 200301010000
    midas_extract get_stations  -b 52,52.2,0.2,0.4 -s 200301010000 -d rain
    midas_extract get_stations  -b 52,52.2,0.2,0.4 -s 199901010000 -e 200501010000 -d rain
    midas_extract get_stations  -c DEVON -s 199901010000 -e 200501010000 -d rain
    midas_extract get_stations  -c DEVON  -e 200501010000 -d rain

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
        start = long(start)
    if end:
        end = long(end)

    if not data_type:
        data_type = []
    else:
        data_type = data_type.split(',')

    if not county and not bbox:
        raise click.ClickException("You must provide a miminum of either a list of counties or " \
                                   "bbox coordinates.")

    return StationIDGetter(county, bbox, data_type, start, end, output_filepath, quiet)


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
