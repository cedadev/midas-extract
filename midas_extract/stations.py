"""
stations.py
===========

Holds StationIDGetter class for finding a list of station ID based on a set of filters.

"""

# Import required modules
import os
import re
import sys
import glob


from midas_extract import bbox_utils
from midas_extract import settings


# Set up global variables
metadata_dir = settings.METADATA_DIR
source_file = os.path.join(metadata_dir, "SRCE", "SRCE.DATA.COMMAS_REMOVED")
source_cols_file = os.path.join(metadata_dir, "table_structures", "SRTB.txt")
source_capabilities_file = os.path.join(metadata_dir, "SRCC", "SRCC.DATA")
source_caps_cols_file = os.path.join(metadata_dir, "table_structures", "SCTB.txt")

geog_area_file = os.path.join(metadata_dir, "GEAR", "GEAR.DATA")
geog_area_cols_file = os.path.join(metadata_dir, "table_structures", "GEOGRAPHIC_AREA.txt")

_date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})\s*(\d{2})?:?(\d{2})?")


def date_match(line, pattern):
    """
    If line matches pattern then return the date as an integer, else None.
    """
    match = pattern.match(line)
    if match:
        d = "".join([m for m in match.groups() if m])
        while len(d) < 12:
            d = d + "00"

        dt = int(d)
        return dt
    return


class StationIDGetter:
    """
    Class to generate lists of station names from arguments.
    """

    def __init__(self, counties, bbox, start_time, end_time, data_type=None, 
                 output_file=None, quiet=None):
        """
        Sets up instance variables and calls relevant methods.
        """
        if not data_type:
            self.data_type = []
        else: 
            self.data_type = [dtype.lower() for dtype in data_type]

        # fix times to ensure correct formats (integers)
        if type(start_time) == type("str"):
            start_time = start_time.replace("T", " ")
            start_time = date_match(start_time, _date_pattern)

        if type(end_time) == type("str"):
            end_time = end_time.replace("T", " ")
            end_time = date_match(end_time, _date_pattern)

        self.start_time = start_time
        self.end_time = end_time

        # Read in tables
        self.build_tables()

        # Do spatial search to get a load of SRC_IDs
        if counties == []:
            st_list = self._get_by_bbox(bbox)
        else:
            counties = [county.upper() for county in counties]
            st_list = self._get_by_county(counties)

        # Now do extra filtering
        self.st_list = self._filter_by_src_caps(st_list)

        print("Number of stations found: {}\n".format(len(self.st_list)))

        if not quiet:
            print("SRC IDs follow:\n==================")

        if not output_file:
            if not quiet:
                for row in self.st_list:
                    print(row)
        else:
            with open(output_file, "w") as output:
                for row in self.st_list:
                    output.write(row + "\r\n")

            print("Output written to '{}'".format(output_file))

    def get_station_list(self):
        """
        Returns the list.
        """
        return self.st_list

    def _get_by_bbox(self, bbox):
        """
        Returns all stations within a bounding box described as
        [N, W, S, E].
        """
        n, w, s, e = [float(_) for _ in bbox]
        print(f"Searching within a box of (N - S) {n} - {s} and (W - E) {w} - {e}...")

        # Reverse north and south if necessary
        if n < s:
            ntemp = n
            n = s
            s = ntemp

        source = self.tables["SOURCE"]
        sourceCols = source["columns"]
        latCol = self._get_column_index(sourceCols, "HIGH_PRCN_LAT")
        lonCol = self._get_column_index(sourceCols, "HIGH_PRCN_LON")
        srcIDCol = self._get_column_index(sourceCols, "SRC_ID")

        matchingStations = []
        for station in source["rows"]:
            station_list = [item.strip() for item in station.split(",")]

            try:
                lat = float(station_list[latCol])
                lon = float(station_list[lonCol])
            except:
                try:
                    lat = float(station_list[latCol] + 1)
                    lon = float(station_list[lonCol] + 1)
                except:
                    print(station)

            src_id = station_list[srcIDCol]

            if bbox_utils.is_in_bbox(lat, lon, n, w, s, e):
                matchingStations.append(src_id)

        return matchingStations

    def _filter(self, rows, term):
        """
        Returns a reduced list of rows that match the term given.
        """
        new_rows = []

        for row in rows:
            if row.find(term) > -1:
                new_rows.append(row)

        return new_rows

    def _get_by_county(self, counties):
        """
        Returns all stations within the borders of the counties listed.
        """
        print("\nCOUNTIES to filter on: {}".format(counties))

        source = self.tables["SOURCE"]
        sourceCols = source["columns"]
        geog = self.tables["GEOG"]
        geogCols = geog["columns"]

        area_type_col = self._get_column_index(geogCols, "GEOG_AREA_TYPE")
        areaIDCol = self._get_column_index(geogCols, "WTHN_GEOG_AREA_ID")
        area_name_col = self._get_column_index(geogCols, "GEOG_AREA_NAME")

        sourceAreaIDCol = self._get_column_index(sourceCols, "LOC_GEOG_AREA_ID")
        srcIDCol = self._get_column_index(sourceCols, "SRC_ID")

        countyCodes = []
        countyMatches = []

        for area in geog["rows"]:

            area_list = [a.strip() for a in area.split(",")]
            areaID = area_list[areaIDCol]

            area_type = area_list[area_type_col]
            area_name = area_list[area_name_col]

            if area_type.upper() == "COUNTY" and area_name in counties:

                countyCodes.append(areaID)

        matchingStations = []

        for station in source["rows"]:

            items = [item.strip() for item in station.split(",")]
            if items[sourceAreaIDCol] in countyCodes:
                matchingStations.append(items[0])

        return matchingStations

    def _filter_by_src_caps(self, st_list):
        """
        Does data type and time range filtering if requested.
        """
        if self.data_type == [] and (self.start_time == None and self.end_time == None):
            return st_list

        if self.data_type != []:
            print("Filtering on data types: {}".format(self.data_type))

        if self.start_time:
            print("From: {}".format(self.start_time))

        if self.end_time:
            print("To: {}".format(self.end_time))

        new_list = []

        srcc = self.tables["SRCC"]
        srccRows = srcc["rows"]
        srccCols = srcc["columns"]

        idTypeCol = self._get_column_index(srccCols, "ID_TYPE")
        srcIDCol = self._get_column_index(srccCols, "SRC_ID")

        startCol = self._get_column_index(srccCols, "SRC_CAP_BGN_DATE")
        endCol = self._get_column_index(srccCols, "SRC_CAP_END_DATE")

        for row in srccRows:

            items = [item.strip() for item in row.split(",")]
            srcID = items[srcIDCol]

            if srcID in st_list:

                # Check if this data type includes this source id
                data_type_allowed = False

                if self.data_type != []:
                    dataType = items[idTypeCol]

                    if dataType.lower() in self.data_type:
                        data_type_allowed = True

                else:
                    data_type_allowed = True

                # Check if this time window is available for this source id
                time_allowed = True

                if self.start_time:
                    endOfMeasuring = date_match(items[endCol], _date_pattern)

                    if self.start_time > endOfMeasuring:
                        time_allowed = False

                if self.end_time:
                    startOfMeasuring = date_match(items[startCol], _date_pattern)

                    if self.end_time < startOfMeasuring:
                        time_allowed = False

                if data_type_allowed and time_allowed:
                    if srcID not in new_list:
                        new_list.append(srcID)

        print("Original list length: {}".format(len(st_list)))
        print("Selected after SRCC filtering: {}".format(len(new_list)))
        return new_list

    def _line_match(self, line, pattern):
        """
        If line matches pattern then return the date as an integer, else None.
        """
        match = pattern.match(line)

        if match:
            return int("".join(match.groups()[1:]))

        return

    def _get_column_index(self, alist, item):
        """
        Returns the index of item in alist.
        """
        return alist.index(item)

    def build_tables(self):
        """
        Builds some dictionaries to house the tables in the form:
        self.tables["SOURCE"] = {"columns"=["src_id", ...]
                               "rows"=["23942309423.,234,2342","234...]}
        """
        self.tables = {}

        self.tables["SOURCE"] = {"columns": [i.strip() for i in open(source_cols_file).readlines()],
                                 "rows": [i.strip() for i in self._clean_rows(open(source_file).readlines())]}
        self.tables["GEOG"] = {"columns": [i.strip() for i in open(geog_area_cols_file).readlines()],
                               "rows": [i.strip() for i in self._clean_rows(open(geog_area_file).readlines())]}
        self.tables["SRCC"] = {"columns": [i.strip() for i in open(source_caps_cols_file).readlines()],
                               "rows": [i.strip() for i in self._clean_rows(open(source_capabilities_file).readlines())]}

    def _clean_rows(self, rows):
        """
        Returns rows that should have removed any odd SQL headers or footers.
        """
        new_rows = []

        for row in rows:
            if row.find("[") > -1 or row.find("SQL") > -1 or row.find("Oracle") > -1:
                continue

            if row.find(",") > -1:
                new_rows.append(row)

        return new_rows

