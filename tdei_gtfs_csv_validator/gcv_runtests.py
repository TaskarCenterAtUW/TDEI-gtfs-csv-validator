# test fncs for gtfs-csv-validator

# don't like this, but couldn't figure out how to make the paths work
import sys
sys.path.append(".")

import fnmatch
import os as os
import re as re
from tdei_gtfs_csv_validator import gcv_support as gcvsup
from tdei_gtfs_csv_validator import exceptions as gcvex 

def run_tests(data_type, schema_version, dir_path, con):
    print("TEST: begin run_tests")

    # create all tables for this particular data_type
    gcvsup.create_schema_tables(data_type, schema_version, con)
    
    print("TEST: schema tables created")

    # read all files from directory test_files/data_schema/version
    file_list = os.listdir(path = dir_path)

    # probably this should be a function...
    fail = False
    for file_name in file_list:
        if fnmatch.fnmatch(file_name, "*.txt"):
            try:
                # check schema for csv files
                # loads file_name into schema_table checks for errors
                gcvsup.test_csv_file(data_type, file_name,dir_path,con)
            except Exception as err:
                gcvsup.drop_all_tables(data_type, con)
                raise
        elif(data_type == 'gtfs_flex' and fnmatch.fnmatch(file_name, "*.geojson")):
            try:
                # check the geojson file for flex
                gcvsup.check_locations_geojson(data_type, schema_version,dir_path,file_name)
            except Exception as err:
                gcvsup.drop_all_tables(data_type, con)
                raise
        else:
            raise gcvex.UnexpectedDataType()

    print("checking " + data_type + " rules on " + dir_path)
    try:
        gcvsup.check_rules(data_type, schema_version, con)
    except Exception as err:
        gcvsup.drop_all_tables(data_type, con)
        raise

    # command to print out the tables for debugging...
    # gcvsup.print_schema_tables(data_type, con)
    gcvsup.drop_all_tables(data_type, con)