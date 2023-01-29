# test fncs for gtfs-csv-validator

# don't like this, but couldn't figure out how to make the paths work
import sys
sys.path.append(".")

import fnmatch
import os as os
import re as re
from tdei_gtfs_csv_validator import gcv_support as gcvsup
from tdei_gtfs_csv_validator import exceptions as gcvex 

def test_release(data_type, schema_version, dir_path, con):
    gcvsup.gcv_debug("testing release in directory: " + dir_path)

    # create all tables for this particular data_type
    gcvsup.create_schema_tables(data_type, schema_version, con)
    
    gcvsup.gcv_debug("schema tables created")

    # read all files from directory test_files/data_schema/version
    file_list = os.listdir(path = dir_path)

    # Do the schema checks
    fail = False
    error_log = ''
    for file_name in file_list:
        try:
            test_file(data_type, schema_version, file_name, dir_path, con)
        except (gcvex.GCVSchemaTestError, gcvex.GCVGeoJsonCheckError) as err:
            # catch GCV schema test exception
            # add exception message to log with file name
            # continue as long as the exception is a gcv schema test exception
            error_log += str(err)   
            fail = True

    # if schema check failed, pass back log of errors
    if(fail):
        gcvsup.drop_all_tables(data_type, con)
        raise gcvex.GCVSchemaTestError(error_log) 

    # else if schema check passed, now check rules
    gcvsup.gcv_debug("checking " + data_type + " rules on " + dir_path)

    try:
        gcvsup.check_rules(data_type, schema_version, con, dir_path)
    except Exception as err:
        gcvsup.drop_all_tables(data_type, con)
        raise
    else:
        # command to print out the tables for debugging...
        # gcvsup.print_schema_tables(data_type, con)
        gcvsup.drop_all_tables(data_type, con)


def test_file(data_type, schema_version, file_name, dir_path, con):

    if fnmatch.fnmatch(file_name, "*.txt"):
        # check schema for csv files
        # loads file_name into schema_table checks for errors
        gcvsup.test_csv_file(data_type, file_name,dir_path,con)
    elif(data_type == 'gtfs_flex' and fnmatch.fnmatch(file_name, "*.geojson")):
        # check the geojson file for flex
        gcvsup.check_locations_geojson(data_type, schema_version, dir_path,file_name)
    else:
        raise gcvex.GCVUnexpectedDataTypeError('data_type')

