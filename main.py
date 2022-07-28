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
from distutils.log import ERROR
import sqlite3 as sql
from ssl import _create_default_https_context
import pandas as pd

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


# import a csv file into a sqlite database table
# attribute names will be taken from the header row of the csv file 
# this is a generic function which takes any csv file and imports that
# file into a sqlite table - the table will be named with the filename
# of the csv file
# first argument is the name/path of the csvfile to be converted to the table
# second argument is the name of the table to be created
def csv_to_table(file_name, table_name, con):
    # skipinitialspace skips spaces after (comma) delimiters
    # lines that start with # (commented lines) will be ignored 
    df = pd.read_csv(file_name, skipinitialspace='True', comment="#")
    
    # tablename is first argument, returns number of rows
    df.to_sql(table_name, con, if_exists='fail', index=False) 

# takes as input a schema definition csv file and creates a table
# from it, schema is the name of the data schema - should be pathways,
# flex or osw, version is the version number
# this function will read the file schema_version_schema.csv
# to get the schema definition
def create_schema_table(schema_name, con):
    df = pd.read_csv('schemas/' + schema_name + "_schema.csv", skipinitialspace='True', 
        comment='#')
    create_table = "CREATE TABLE '" + schema_name + "'("  
    for row in df.itertuples(index=True, name=None):
        if row[0] != 0:
            create_table += ", "
        create_table += row[1] + " " + row[4]
    create_table += ") strict;"
    cur = con.cursor()
    cur.execute(create_table)

def check_schema(dir_name, file_name, schema_table, con):
    print("Running test on file: " + file_name)
    # check to see if success or fail in file name
    expect_success = True # assume we expect success
    if(re.search('Fail', file_name, re.IGNORECASE) != None):
        expect_success = False # if Fail, fail, or FAIL in file name
    
    # load pathways, flex file into table...
    csv_to_table(dir_name + "/" + file_name, file_name, con)

    cur = con.cursor()
    # catch error - some expected passes, some expected fails
    try:
        cur.execute("insert into '" + schema_table + 
            "' select * from '" + file_name + "'")
    except sql.IntegrityError as err:
        if(expect_success == False):
            print("Success: Test on " + file_name + " failed as expected.")
            print(os.linesep)
        else:
            print("FAIL: Test on " + file_name + " failed, expected to succeed.")
            print(err)
            print(os.linesep)
    else:
        if(expect_success == True):
            print("Success: Test on " + file_name + "succeeded as expected")
            print(os.linesep)
        else:
            print("FAIL: Test on " + file_name + " succeeded, expected to fail.")
            print(os.linesep) 


def check_rules(schema_name, file_name, con):
    print("Checking rules on: " + file_name)
    df = pd.read_csv('rules/' + schema_name + "_rules", skipinitialspace='True', 
        comment='#')
    cur = con.cursor()

    for row in df.itertuples(index=True, name=None):
        # for each line - read sql, execute sql on appropriate table (tablename?)
        rule_name = row[1]
        fail_msg = row[2]
        rule_sql = row[3]    
        print("Checking rule: " + rule_name)

        # use regex sub to replace TABLE with tablename
        print(rule_sql)
        rule_sql = re.sub('TABLE', file_name, rule_sql)    
        cur.execute(rule_sql)
        row = cur.fetchone()
        if row is not None:
            print("FAIL:" + rule_name + " failed " + fail_msg)
        else:
            print("Success: " + rule_name + " succeeded")

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

schema_table = data_schema + "_" + version
create_schema_table(schema_table, con)

def test_script(data_schema, version, schema_table, con):
    # read all files from directory test_files/data_schema/version
    dir_name = 'test_files/' + data_schema + '/' + version
    file_list = os.listdir(path = dir_name)

    for file_name in file_list:
        # check schema
        # loads file_name into schema_table checks for errors
        check_schema(dir_name, file_name, schema_table, con)
        check_rules(schema_table, file_name, con)

    # when all tests are done, drop tuples from the table
    cur.execute("delete from '" + schema_table + "'")

  
#    for row in cur.execute("SELECT * FROM '" + schema_name + "'"):
#        print(row)

print("DONE")


con.close()



