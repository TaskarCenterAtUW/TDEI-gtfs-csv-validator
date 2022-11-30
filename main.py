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



# Use cases
# 1. Test a single file - specify: schema_type, file_type, file_path
# 2. Test a release - specify schema_type, directory_path
# 3. Run this script using the provided test files for a file_type
# 4. Run this script using the provided test files for a schema type 
# Note: 3 and 4 also function to test this script

# script params
# test_type = 'file' or 'release' or 'script-file' or 'script-release' 
# schema_type = 'pathways' or 'flex'
# schema_version = version of schema to be tested against
# file_type = 'pathways.txt', 'levels.txt', etc. (for file and script-file only)
# path = path to file for file, path to directory for release, ignored for script-* tests

# set the params here until I learn how to add params to a python function
data_type = 'gtfs_pathways'
schema_version = 'v1.0'
dir_path = 'test_files/gtfs_pathways/v1.0/success_1_all_attrs' 

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

print("Calling run_tests")
gcvtests.run_tests(data_type, schema_version, dir_path, con)

print("ALL DONE")
con.close()




