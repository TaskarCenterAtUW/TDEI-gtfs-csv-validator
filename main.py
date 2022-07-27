# gtfs-csv-validator
# validates csv gtfs files versus a specified schema - which is either the
# gtfs schema for that type of file or an extension of the gtfs schema for
# that type of file
# schema is specified as a three-column csv file (name, type, Required)
# mappings from gtfs types to database types are kept in a csv file which is part of 
# this repo


# steps
# import gtfs_to_db_types into a sqlite table (gtfs_types)
# import schema file into a sqlite table (e.g. pathways_schema, levels_schema, etc...)
# create table based on types and schema tables just created that captures 
# the gtfs schema requirements for the particular gtfs table
# e.g. a table named pathways_schema will capture the gtfs requirements for a
# pathways.txt file

import sqlite3 as sql
import pandas as pd

print("hello world")

