# -*- coding: utf-8 -*-

"""Console script for midas_extract."""

__author__ = """Ag Stephens"""
__contact__ = "ag.stephens@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__version__ = "0.1.0"

import sys
import click


@click.command()
def main(args=None):
    """Console script for midas_extract."""
    click.echo("Replace this message by putting your code into "
               "midas_extract.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
