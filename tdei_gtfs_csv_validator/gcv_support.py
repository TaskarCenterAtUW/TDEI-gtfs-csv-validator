# support functions for gtfs-csv-validator

import sys
sys.path.append(".")

import os as os
import re as re
import sqlite3 as sql
import pandas as pd
from tdei_gtfs_csv_validator import exceptions as gcvex 
from jsonschema import validate as jsvalidate
import json

# Uses: https://github.com/python-jsonschema/jsonschema

# import a csv file into a sqlite database table
# attribute names will be taken from the header row of the csv file 
# this is a generic function which takes any csv file and imports that
# file into a sqlite table - the table will be named with the filename
# of the csv file
# first argument is the name/path of the csvfile to be converted to the table
# second argument is the name of the table to be created
def csv_to_table(file_name, table_name, con):
    gcv_debug("csv_to_table",2)
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
def create_schema_tables(data_type, schema_version, con):
    gcv_debug("begin create_schema_tables")

    dir_path = 'schemas/' + data_type + "/" + schema_version + "/"
    table_names = []
    if(data_type == 'gtfs_pathways'):
        table_names = ["levels", "pathways", "stops"]
    elif(data_type == 'gtfs_flex'):
        table_names = ["booking_rules", "location_groups", "stop_times"]
    else:
        raise RuntimeError("unexpected data type")


    for table_name in table_names:
        file_path = dir_path + table_name + "_schema.csv"
        gcv_debug("reading file " + file_path,2) 
        df = pd.read_csv(file_path, skipinitialspace='True', comment='#')
        create_table = "CREATE TABLE '" + table_name + "'("  
        for row in df.itertuples(index=True, name=None):
            if row[0] != 0:
                create_table += ", "
            create_table += row[1] + " " + row[4]
        create_table += ") strict;"
      
        gcv_debug("query: " + create_table,2)
        try:
            cur = con.cursor()
            cur.execute(create_table)
        except Exception as excep:
            gcv_debug(excep)
            raise excep
        gcv_debug("schema table " + table_name + " created")
    
    gcv_debug("schema_tables created")


# this function takes the name of the test and the file name and
# checks to see if the file is expected to fail or pass this test
# returns yes if success is expected, no if file is expected to fail
# the test
def check_expect_success(test_name, file_name):
    # expect fail if we have Fail, fail or FAIL and the test name in the file name
    if(re.search('Fail', file_name, re.IGNORECASE) != None and 
        re.search(test_name, file_name) != None):
            return False; # if Fail, fail, or FAIL in file name
    return True;


def check_schema(file_path, schema_table, file_table, con):
    gcv_debug("TEST: Checking schema: ")
    # check to see if success or fail in file name
    expect_success = check_expect_success('schema', file_path)

    # load pathways, flex file into table...
    csv_to_table(file_path, file_table, con)

    cur = con.cursor()

    # figure out which attributes exist in the csv file
    # and create the appropriate insert command
    # get list of col names from schema_table
    # get list of col names from file_name (table)
    # one optoin - PRAGMA table_info(foo)
    # schema table is strange  
    schema_table_info = cur.execute("PRAGMA table_info('" + schema_table + "')").fetchall()
    file_name_info = cur.execute("PRAGMA table_info('" + file_table + "')").fetchall()

    # table_info returns lists of tuples - each row in that list 
    # represents one attr, I want the attr name, which is col 1
    schema_table_attrs = [tuple[1] for tuple in schema_table_info]
    file_name_attrs = [tuple[1] for tuple in file_name_info]

    query = "insert into '" + schema_table + "' select "
    first_attr = True
    for attr in schema_table_attrs:
        if(first_attr == True):
            first_attr = False
        else:
            query += ', '
        
        if(attr in file_name_attrs):  
            query += attr 
        else:
            query += "NULL"

    # add end of query
    query += " from " + file_table 

    gcv_debug(query,2)

    # catch error - some expected passes, some expected fails
    fail = False
    try:
        cur.execute(query)
    except sql.IntegrityError as err:
        if(expect_success == False):
            gcv_debug("\tSuccess: Schema check failed as expected.")
        else:
            gcv_debug("\tFAIL: Schema check failed, expected to succeed.")
            gcv_debug("\t\t", err)
            fail = True
    except sql.OperationalError as err:
        if(expect_success == False):
            gcv_debug("\tSuccess: Schema check failed as expected.")
        else:
            gcv_debug("\tFAIL: Schema check failed, expected to succeed.")
            gcv_debug("\t\t", err)
            fail = True
    except Exception as err:
        gcv_debug(f"unexpected {err=}, {type(err)=}") 
        raise
    else:
        if(expect_success == True):
            gcv_debug("\tSuccess: Schema check succeeded as expected")
        else:
            gcv_debug("\tFAIL: Schema check succeeded, expected to fail.")
            fail = True
    
    if(fail == True):
        raise gcvex.TestFailed("schema check failed")


def check_rules(data_type, schema_version, con):
    gcv_debug("TEST: begin check rules") 
    rules_file = 'rules/' + data_type + "_" + schema_version + "_rules.csv"
    df = pd.read_csv(rules_file, skipinitialspace='True', 
        comment='#')
    cur = con.cursor()

    for row in df.itertuples(index=True, name=None):
        # for each line - read sql, execute sql on appropriate table (tablename?)
        rule_name = row[1]
        fail_msg = row[2]
        rule_sql = row[3]    
        gcv_debug("\tChecking rule: " + rule_name)
        
        gcv_debug("Rule sql: " + rule_sql,2)
        try:
            cur.execute(rule_sql) 
        except Exception as err:
            gcv_debug("unexpected query execution error")
            gcv_debug(err)
            raise 
            
        row = cur.fetchone()
        if row is not None:
            gcv_debug("\t\tFAIL:" + rule_name + " failed " + fail_msg)
            gcv_debug("Failing row:")
            gcv_debug(row)
            raise gcvex.TestFailed("test " + rule_name + "failed")
        else:
            gcv_debug("\t\tSuccess: " + rule_name + " succeeded")

def print_schema_tables(data_type, con):
    cur = con.cursor()
    table_names = []
    if(data_type == 'gtfs_pathways'):
        table_names = ["levels", "pathways", "stops"]
    elif(data_type == 'gtfs_flex'):
        table_names = ["booking_rules", "location_groups", "stop_times"]
    else:
        raise gcvex.UnexpectedDataType()

    for table_name in table_names:
        cur.execute("Select * from " + table_name)
        gcv_debug(cur.fetchall())


def drop_all_tables(data_type, con):
    cur = con.cursor()
    table_names = []
    if(data_type == 'gtfs_pathways'):
        table_names = ["levels", "pathways", "stops", "levels_file", "pathways_file", "stops_file"]
    elif(data_type == 'gtfs_flex'):
        table_names = ["booking_rules", "location_groups", "stop_times"]
    else:
        raise gcvex.UnexpectedDataType()
    
    for table_name in table_names:
        cur.execute("drop table " + table_name)
    
def check_locations_geojson(data_type, schema_version, idir_path, ifile_name):
    gcv_debug("TEST: Testing geojson file: " + ifile_name)

    expect_success = check_expect_success('schema', ifile_name)
        
    # get jsonschema for flex locations.geojson file
    sdir_path = 'schemas/' + data_type + "/" + schema_version + "/"
    sfile_path = sdir_path + "locations_geojson_jsonschema.json" 
    jsonschema_file = open(sfile_path, "r")
    locations_schema = json.load(jsonschema_file)
    jsonschema_file.close()
    gcv_debug(locations_schema,2)

    ifile_path = idir_path + "/" + ifile_name 
    ijsonschema_file = open(ifile_path, "r")
    locations_instance = json.load(ijsonschema_file)
    ijsonschema_file.close()

    try:
        jsvalidate(locations_instance, locations_schema)
        #jsvalidate(instance={"name" : "Eggs", "price" : 34.99}, 
        #            schema=locations_schema)
    except Exception as err:
        if(expect_success == False):
            gcv_debug("\tSuccess: geojson schema check failed as expected.")
        else:
            raise gcvex.TestFailed("test schema check on locations.geojson failed")
    else:
        gcv_debug("flex locations geojson test succeeded")


def test_csv_file(data_type,file_name,dir_path,con):
    gcv_debug("TEST: Testing csv file: " + file_name)
    # data_type is pathways, or flex 
    if(data_type == 'gtfs_pathways'):
        if(re.search('levels', file_name, re.IGNORECASE) != None):  
            schema_table = 'levels'
            file_table = 'levels_file'
        elif(re.search('pathways', file_name, re.IGNORECASE) != None):  
            schema_table = 'pathways'
            file_table = 'pathways_file'
        elif(re.search('stops', file_name, re.IGNORECASE) != None):  
            schema_table = 'stops'
            file_table = 'stops_file'
    elif(data_type == 'gtfs_flex'):
        if(re.search('booking_rules', file_name, re.IGNORECASE) != None):  
            schema_table = 'booking_rules'
            file_table = 'booking_rules_file'
        elif(re.search('location_groups', file_name, re.IGNORECASE) != None):  
            schema_table = 'location_groups'
            file_table = 'location_groups_file'
        elif(re.search('stop_times', file_name, re.IGNORECASE) != None):  
            schema_table = 'stop_times'
            file_table = 'stops_times_file'
    else:
        raise AssertionError('only flex and pathways supported')
        
    # file_path, data_type, con
    file_path = dir_path + '/' + file_name
    check_schema(file_path, schema_table, file_table, con)

# debug_log function provides internal support for debugging for the gcv
# intended use is to replace the internals of this function with code 
# to handle debug messages as the dev wants - for example - print statement
# to print debug info to console or leave empty to have no debug messages
# allows multiple levels of priority...
def gcv_debug(log_msg, priority=1):
    """function to support debugging messages for the gcv""" 
    #if(priority == 1):
    #    print(log_msg)

# debug_log function provides internal support for logging for the gcv
# intended use is to replace the internals of this function with code 
# to handle log messages - expect to replace this empty function with 
# calls to logging in the core library
def gcv_log(log_msg):
    """function to support logging for gcv"""

