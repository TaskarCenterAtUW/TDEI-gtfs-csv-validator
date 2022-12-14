# gtfs-csv-validator
# validates csv gtfs files versus a specified schema - which is either the
# gtfs schema for that type of file or an extension of the gtfs schema for
# that type of file
# schema is specified as a four-column csv file (name, type, Required,sqlite_type)

# Summary
# imports schema file into a sqlite table (e.g. pathways_schema, levels_schema, etc...)
# the sqlite table captures many of the gtfs schema requirements for that 
# particular gtfs table
# reads a list of test files
# imports those test files into sqlite tables and tries to insert
# data from those tables into the schema table - checks for schema issues

# TODOS: 
# set up flex validation schemas
# test a real pathways file 

# need to verify IDs are UTF-8 characters?

# new rules needed:
# pathways rules are graph traversals - need to add checks for those
# fks to be enforced with rules or somesuch

import re as re
import sqlite3 as sql
import gcv_testfcns as gcvtests



# Use of script: Test a release - specify data_type, schema_version
# and a (list of) test directories 

# script params
# data_type = 'gtfs_pathways' or 'gtfs_flex'
# schema_version = version of schema to be tested against 
#        use v1.0 for pathways tests or v2.0 for flex tests
# test_dirs = a list of directories to be tested, each directory 
#             is expected to contain a release for the data_type 
#             specified. gtfs_pathways expects levels, pathways and 
#             stops files. gtfs_flex expects booking_rules, loction_groups
#             and stop_times files

# set the params here until I learn how to add params to a python function
data_type = 'gtfs_pathways' # or 'gtfs-flex' for flex
schema_version = 'v1.0' # or 'v2.0' for flex

#data_type = 'gtfs_flex'
#schema_version = 'v2.0'

#test_dirs = ['test_files/gtfs_pathways/v1.0/success_1_all_attrs',
#             'test_files/gtfs_pathways/v1.0/success_2_missing_attrs',
#             'test_files/gtfs_pathways/v1.0/fail_schema_1']

#test_dirs = ['test_files/gtfs_pathways/v1.0/success_1_all_attrs']
#test_dirs = ['test_files/gtfs_pathways/v1.0/success_2_missing_attrs']
#test_dirs = ['test_files/gtfs_pathways/v1.0/fail_schema_1']
#test_dirs = ['test_files/gtfs_pathways/v1.0/mbta_20220920_small']
test_dirs = ['test_files/gtfs_pathways/v1.0/mbta_20220920']

#test_dirs = ['test_files/gtfs_flex/v2.0/success_1_all_attrs']

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

for dir_path in test_dirs:  
    print("Calling run_tests on " + dir_path)
    try:
        gcvtests.run_tests(data_type, schema_version, dir_path, con)
    except Exception as excep:
        print(excep)
        print("TEST FAILED - see trace messages")
    else:
        print("TEST SUCCEEDED - ALL DONE")

con.close()




