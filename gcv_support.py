# support functions for gtfs-csv-validator

import os as os
import re as re
import sqlite3 as sql
import pandas as pd

# import a csv file into a sqlite database table
# attribute names will be taken from the header row of the csv file 
# this is a generic function which takes any csv file and imports that
# file into a sqlite table - the table will be named with the filename
# of the csv file
# first argument is the name/path of the csvfile to be converted to the table
# second argument is the name of the table to be created
def csv_to_table(file_name, table_name, con):
    #print("csv_to_table")
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
    print("begin create_schema_tables")

    dir_path = 'schemas/' + data_type + "/" + schema_version + "/"
    if(data_type == 'gtfs_pathways'):
        file_names = ["levels_schema", "pathways_schema", "stops_schema"]
        for file_name in file_names:
            print("reading file " + dir_path + file_name + ".csv")
            df = pd.read_csv(dir_path + file_name + ".csv", skipinitialspace='True', comment='#')
            create_table = "CREATE TABLE '" + file_name + "'("  
            for row in df.itertuples(index=True, name=None):
                if row[0] != 0:
                    create_table += ", "
                create_table += row[1] + " " + row[4]
            create_table += ") strict;"
            try:
                cur = con.cursor()
                cur.execute(create_table)
            except Exception as excep:
                print(excep)

    else:
        print("gtfs_flex not supported yet")
    
    print("end create_schema_tables")


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
    print("TEST: Checking schema: ")
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
            query += ", "
        if(attr in file_name_attrs):
            query += attr
        else:
            query += '1'
        

    # add end of query
    query += " from " + file_table 

    print(query)

    # catch error - some expected passes, some expected fails
    try:
        cur.execute(query)

    except sql.IntegrityError as err:
        if(expect_success == False):
            print("\tSuccess: Schema check failed as expected.")
        else:
            print("\tFAIL: Schema check failed, expected to succeed.")
            print("\t\t", err)
    else:
        if(expect_success == True):
            print("\tSuccess: Schema check succeeded as expected")
        else:
            print("\tFAIL: Schema check succeeded, expected to fail.")


def check_rules(schema_name, file_name, con):
    print("TEST: Checking rules on: " + file_name)
    df = pd.read_csv('rules/' + schema_name + "_rules", skipinitialspace='True', 
        comment='#')
    cur = con.cursor()

    for row in df.itertuples(index=True, name=None):
        # for each line - read sql, execute sql on appropriate table (tablename?)
        rule_name = row[1]
        fail_msg = row[2]
        rule_sql = row[3]    
        print("\tChecking rule: " + rule_name)
        
        print(rule_sql)
        cur.execute(rule_sql) 
        row = cur.fetchone()
        if row is not None:
            print("\t\tFAIL:" + rule_name + " failed " + fail_msg)
        else:
            print("\t\tSuccess: " + rule_name + " succeeded")



