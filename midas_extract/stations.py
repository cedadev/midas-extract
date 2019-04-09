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


import bbox_utils
import settings


# Set up global variables
metadata_dir = settings.METADATA_DIR
source_file = os.path.join(metadata_dir, "SRCE.DATA.COMMAS_REMOVED")
source_cols_file = os.path.join(metadata_dir, "SOURCE.txt")
source_capabilities_file = os.path.join(metadata_dir, "SRCC.DATA")
source_caps_cols_file = os.path.join(metadata_dir, "table_structures", "SCTB.txt")

geog_area_file = os.path.join(metadata_dir, "GEAR.DATA")
geog_area_cols_file = os.path.join(metadata_dir, "GEOGRAPHIC_AREA.txt")

_date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})\s*(\d{2})?:?(\d{2})?")


def date_match(line, pattern):
    """
    If line matches pattern then return the date as a long, else None.
    """
    match = pattern.match(line)
    if match:
        d = "".join([m for m in match.groups() if m])
        while len(d) < 12:
            d = d + "00"

        dt = long(d)
        return dt
    return


class StationIDGetter:
    """
    Class to generate lists of station names from arguments.
    """

    def __init__(self, counties, bbox, data_types, start_time, end_time, output_file=None, noprint=None):
        """
        Sets up instance variables and calls relevant methods.
        """
        self.data_types = [dtype.lower() for dtype in data_types]

        # fix times to ensure correct formats (longs)
        if type(start_time) == type("str"):
            start_time = start_time.replace("T", " ")
            start_time = date_match(start_time, _date_pattern)

        if type(end_time) == type("str"):
            end_time = end_time.replace("T", " ")
            end_time = date_match(end_time, _date_pattern)

        self.start_time = start_time
        self.end_time = end_time

        # Read in tables
        self._buildTables()

        # Do spatial search to get a load of SRC_IDs
        if counties == []:
            st_list = self._getByBBox(bbox)
        else:
            counties = [county.upper() for county in counties]
            st_list = self._getByCounties(counties)

        # Now do extra filtering
        self.st_list = self._filterBySourceCapability(st_list)

        print("Number of stations found: {}\n".format(len(self.st_list)))

        if noprint == None:
            print("SRC IDs follow:\n==================")
        if output_file == None:
            if noprint == None:
                for row in self.st_list:
                    print(row)
        else:
            output = open(output_file, "w")

            for row in self.st_list:
                output.write(row + "\r\n")

            output.close()

            print("Output written to '{}'".format(output_file))

    def getStationList(self):
        """
        Returns the list.
        """
        return self.st_list

    def _getByBBox(self, bbox):
        """
        Returns all stations within a bounding box described as
        [N, W, S, E].
        """
        (n, w, s, e) = bbox
        print "Searching within a box of (N - S) %s - %s and (W - E) %s - %s..." % (
            n, s, w, e)
        n = float(n)
        w = float(w)
        s = float(s)
        e = float(e)

        # Reverse north and south if necessary
        if n < s:
            ntemp = n
            n = s
            s = ntemp

        source = self.tables["SOURCE"]
        sourceCols = source["columns"]
        latCol = self._getColumnIndex(sourceCols, "HIGH_PRCN_LAT")
        lonCol = self._getColumnIndex(sourceCols, "HIGH_PRCN_LON")
        srcIDCol = self._getColumnIndex(sourceCols, "SRC_ID")

        matchingStations = []
        for station in source["rows"]:
            stationList = [item.strip() for item in station.split(",")]

            try:
                lat = float(stationList[latCol])
                lon = float(stationList[lonCol])
            except:
                try:
                    lat = float(stationList[latCol]+1)
                    lon = float(stationList[lonCol]+1)
                except:
                    print station

            src_id = stationList[srcIDCol]
            if bbox_utils.isInBBox(lat, lon, n, w, s, e):
                matchingStations.append(src_id)

        return matchingStations

    def _filter(self, rows, term):
        """
        Returns a reduced list of rows that match the term given.
        """
        newRows = []

        for row in rows:
            if row.find(term) > -1:
                newRows.append(row)

        return newRows

    def _getByCounties(self, counties):
        """
        Returns all stations within the borders of the counties listed.
        """
        print "\nCOUNTIES to filter on:", counties

        source = self.tables["SOURCE"]
        sourceCols = source["columns"]
        geog = self.tables["GEOG"]
        geogCols = geog["columns"]

        areaTypeCol = self._getColumnIndex(geogCols, "GEOG_AREA_TYPE")
        areaIDCol = self._getColumnIndex(geogCols, "WTHN_GEOG_AREA_ID")
        areaNameCol = self._getColumnIndex(geogCols, "GEOG_AREA_NAME")

        sourceAreaIDCol = self._getColumnIndex(sourceCols, "LOC_GEOG_AREA_ID")
        srcIDCol = self._getColumnIndex(sourceCols, "SRC_ID")

        countyCodes = []
        countyMatches = []

        for area in geog["rows"]:

            areaList = [a.strip() for a in area.split(",")]
            areaID = areaList[areaIDCol]

            areaType = areaList[areaTypeCol]
            areaName = areaList[areaNameCol]

            if areaType.upper() == "COUNTY" and areaName in counties:

                countyCodes.append(areaID)
#                countyMatches.append(re.compile(r"\s*([^,]+),\s*([^,]+,\s*){%s}(%s,)" % ((sourceAreaIDCol-1), areaID)))
#                print r"([^,]+), ([^,]+, ){%s}(%s,)" % ((sourceAreaIDCol-1), areaID)

        matchingStations = []

        for station in source["rows"]:

            items = [item.strip() for item in station.split(",")]
            if items[sourceAreaIDCol] in countyCodes:
                matchingStations.append(items[0])

            # for cm in countyMatches:
            #    match = cm.match(station)

            #    if match:
            #        src_id = match.group(1)
            #        matchingStations.append(src_id)

        return matchingStations

    def _filterBySourceCapability(self, st_list):
        """
        Does data type and time range filtering if requested.
        """
        if self.data_types == [] and (self.start_time == None and self.end_time == None):
            return st_list

        if self.data_types != []:
            print "Filtering on data types: %s" % self.data_types
        if self.start_time:
            print "From: %s" % self.start_time
        if self.end_time:
            print "To: %s" % self.end_time

        new_list = []

        srcc = self.tables["SRCC"]
        srccRows = srcc["rows"]
        srccCols = srcc["columns"]

        idTypeCol = self._getColumnIndex(srccCols, "ID_TYPE")
        srcIDCol = self._getColumnIndex(srccCols, "SRC_ID")

        startCol = self._getColumnIndex(srccCols, "SRC_CAP_BGN_DATE")
        endCol = self._getColumnIndex(srccCols, "SRC_CAP_END_DATE")

        for row in srccRows:

            items = [item.strip() for item in row.split(",")]
            srcID = items[srcIDCol]

            if srcID in st_list:

                # Check if this data type includes this source id
                data_type_allowed = False

                if self.data_types != []:
                    dataType = items[idTypeCol]

                    if dataType.lower() in self.data_types:
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

    def _lineMatch(self, line, pattern):
        """
        If line matches pattern then return the date as a long, else None.
        """
        match = pattern.match(line)

        if match:
            dateLong = long("".join(match.groups()[1:]))
            return dateLong

        return

    def _getColumnIndex(self, alist, item):
        """
        Returns the index of item in alist.
        """
        return alist.index(item)

    def _buildTables(self):
        """
        Builds some dictionaries to house the tables in the form:
        self.tables["SOURCE"] = {"columns"=["src_id", ...]
                               "rows"=["23942309423.,234,2342","234...]}
        """
        self.tables = {}

        self.tables["SOURCE"] = {"columns": [i.strip() for i in open(source_cols_file).readlines()],
                                 "rows": [i.strip() for i in self._cleanRows(open(source_file).readlines())]}
        self.tables["GEOG"] = {"columns": [i.strip() for i in open(geog_area_cols_file).readlines()],
                               "rows": [i.strip() for i in self._cleanRows(open(geog_area_file).readlines())]}
        self.tables["SRCC"] = {"columns": [i.strip() for i in open(source_caps_cols_file).readlines()],
                               "rows": [i.strip() for i in self._cleanRows(open(source_capabilities_file).readlines())]}

    def _cleanRows(self, rows):
        """
        Returns rows that should have removed any odd SQL headers or footers.
        """
        newRows = []

        for row in rows:
            if row.find("[") > -1 or row.find("SQL") > -1 or row.find("Oracle") > -1:
                continue

            if row.find(",") > -1:
                newRows.append(row)

        return newRows

