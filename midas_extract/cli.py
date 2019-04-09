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
