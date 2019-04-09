# -*- coding: utf-8 -*-

"""Console script for midas_extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import sys
import click

from settings import START_DEFAULT, END_DEFAULT


@click.group()
def main():
   pass


@main.command()
@click.argument('output_filepath')
@click.option('--county', '-c', default=None, help='Comma-separated county list')
@click.option('--bbox', '-b', default=None, help='Bounding box as: N,W,S,E')
@click.option('--quiet', '-q', default=False, help='Quiet mode (do not print to termindal')
@click.option('--counties-file', '-f', default=None, help='Location of counties file, one per line')
@click.option('--start', '-s', default=None, help='Start datetime as: YYYYMMDDhhmm')
@click.option('--end', '-e', default=None, help='End datetime as: YYYYMMDDhhmm') 
@click.option('--data-type', '-d', default=None, help='List of data types')
def get_stations(output_filepath, county=None, bbox=None, quiet=False, counties_file=None,
                 start=None, end=None, data_type=None):
    """
    Takes a county or list of counties and returns a list of station IDs (src_id).
    """
    if county:
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

    if data_type:
        data_type = data_type.split(',')

    if counties == [] and not bbox:
        raise click.ClickException("You must provide a miminum of either a list of counties or " \
                                   "bbox coordinates.")


    return StationIDGetter(county, bbox, data_type, start, end, output_filepath, noprint=(not quiet)) 

"""
    Usage
    =====

    getStations.py [-c <county1>[,<county2>...]] [-x <lon1>,<lon2> -y <lat1>,<lat2>]
                   [-n] [-f <filename>] [-s <YYYYMMDDhhmm>] [-e <YYYYMMDDhhmm>]
                   [-d <datatype>] <output_filename>

Where:
======

    -c      is used followed by a list of counties to match.
    -b      is a bounding box defined as:  N,S,W,E
    -n      do not display any output
    -f      provide a file with a list of counties, one per line
    -s      is the start date-time that you are interested in
    -e      is the end date-time that you are interested in
    -d      is a comma-separated list of data types you want to match (currently
            believed to be CLBD CLBN CLBR CLBW DCNN FIXD ICAO LPMS RAIN SHIP WIND WMO).
    <output_filename>   is used if you want to write the output to a file.


Examples:
=========

    python getStations.py -c cornwall,devon,wiltshire
    python getStations.py  -b 52,54,0,3
    python getStations.py  -b 52,54,0,3 -n
    python getStations.py  -b 52,52.2,0.2,0.4 -s 200301010000
    python getStations.py  -b 52,52.2,0.2,0.4 -s 200301010000 -d rain
    python getStations.py  -b 52,52.2,0.2,0.4 -s 199901010000 -e 200501010000 -d rain
    python getStations.py  -c DEVON -s 199901010000 -e 200501010000 -d rain
    python getStations.py  -c DEVON  -e 200501010000 -d rain

    (args, output_fileList) = getopt.getopt(argList, "c:f:x:y:d:s:e:n")
    counties = []
    noprint = None
    data_types = []
    start_time = None
    end_time = None

    if output_fileList == []:
        output_file = None
    else:
        output_file = output_fileList[0]

    bbox = [None, None, None, None]

    for arg, value in args:
        if arg == "-c":
            counties = value.split(",")
        elif arg == "-x":
            bbox[1], bbox[3] = value.split(",")
        elif arg == "-y":
            bbox[0], bbox[2] = value.split(",")
        elif arg == "-f":
            counties = [line.strip() for line in open(value).readlines()]
        elif arg == "-d":
            data_types = value.split(",")
        elif arg == "-s":
            start_time = long(value)
        elif arg == "-e":
            end_time = long(value)
        elif arg == "-n":
            noprint = 1

    if counties == [] and None in bbox:
        exitNicely(
            "You must provide a miminum of either a list of counties or a x and y box coordinates.")

    StationIDGetter(counties, bbox, data_types, start_time,
                    end_time, output_file, noprint)

    """




if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
