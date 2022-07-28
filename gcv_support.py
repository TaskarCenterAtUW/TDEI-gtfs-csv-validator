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
def create_schema_table(schema_name, con):
    #print("create_schema_table")
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
    print("Checking schema: " + file_name)
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
        else:
            print("FAIL: Test on " + file_name + " failed, expected to succeed.")
            print(err)
    else:
        if(expect_success == True):
            print("Success: Test on " + file_name + " succeeded as expected")
        else:
            print("FAIL: Test on " + file_name + " succeeded, expected to fail.")



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
        sql_file_name = "'" + file_name + "'"
        rule_sql = re.sub('TABLE', sql_file_name, rule_sql)    
        # print(rule_sql)
        cur.execute(rule_sql) 
        row = cur.fetchone()
        print(row)
        if row is not None:
            print("FAIL:" + rule_name + " failed " + fail_msg)
        else:
            print("Success: " + rule_name + " succeeded")



