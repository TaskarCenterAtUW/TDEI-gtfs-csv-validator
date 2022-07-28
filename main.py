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
# need to verify IDs are UTF-8 characters?
# need to add support if pathways data files don't contain all
# fields (that is omit )
# pathways rules are graph traversals - need to add checks for those
# fks to be enforced with rules or somesuch


import os as os
import re as re
#from distutils.log import ERROR
import sqlite3 as sql
#from ssl import _create_default_https_context
import pandas as pd
import gcv_support as sup
import gcv_testfcns as tests


# things that should be params
# test - file, release or script
# if file or release - path to file / directory
# for file - file type (pathways.txt, levels.txt)
# for release - pathways or flex
data_schema = 'pathways' # data type being tested - need to distinguish between
# pathways as a data schema and pathways as a file type
version = 'v1.0' # schema version being tested

# need to think about testing individual files vs testing a release of files
# which is separate from the test structure I created to test this script
# probably need to move the test structure for this script out of
# this script and into a test script...
# think will want this script to be able to test a single file
# or a set of files 

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

schema_table = data_schema + "_" + version
sup.create_schema_table(schema_table, con)

tests.test_script(data_schema, version, schema_table, con)

print("DONE")
con.close()




