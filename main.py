# gtfs-csv-validator
# validates csv gtfs files versus a specified schema - which is either the
# gtfs schema for that type of file or an extension of the gtfs schema for
# that type of file
# schema is specified as a three-column csv file (name, type, Required)
# mappings from gtfs types to database types are kept in a csv file which is part of 
# this repo


# steps
# import gtfs_to_db_types into a sqlite table (gtfs_types)
# how is this mapping stored? in the code? in a file? gtfs types have
# spaces... ugh ... maybe I should just have a command that creates
# a pathways table - screw reading
# import schema file into a sqlite table (e.g. pathways_schema, levels_schema, etc...)
# create table based on types and schema tables just created that captures 
# the gtfs schema requirements for the particular gtfs table
# e.g. a table named pathways_schema will capture the gtfs requirements for a
# pathways.txt file

from distutils.log import ERROR
import sqlite3 as sql
import pandas as pd
import os as os

# things that should be params
data_schema = 'pathways'
version = 'v1.0'


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
    print("csv_to_table " + file_name)
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

    

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

schema_name = data_schema + "_" + version
create_schema_table(schema_name, con)

# read all files from directory test_files/data_schema/version
dir_name = 'test_files/' + data_schema + '/' + version
file_list = os.listdir(path = dir_name)
for file_name in file_list:
    print("Running test on " + file_name)
    # check to see if success or fail in file name
    expect_success = True # if success in file name 
    expect_success = False # if fail in file name
    # check that one and only one of success / fail are in file name

    # load pathways, flex file into table...
    csv_to_table(dir_name + "/" + file_name, file_name, con)

    # catch error - some expected passes, some expected fails
    #try:
    cur.execute("insert into '" + schema_name + 
        "' select * from '" + file_name + "'")
    #        break
    #except # ERROR
        # check if 


    # when all tests are done, drop tuples from the table
    cur.execute("delete from '" + schema_name + "'")

#    for row in cur.execute("SELECT * FROM '" + schema_name + "'"):
#        print(row)


con.close()

# so I can use STRICT to have checking done on insert
# or PRAGMA integrity_check (tablename) to have a table checked 
# need to verify IDs are UTF-8 characters?
# fks to be enforced with rules or somesuch


#csv_to_table('test_files/test.csv', con)
#for row in cur.execute('SELECT * FROM testtable where c = 6'):
#    print(row)
