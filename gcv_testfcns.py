# test fncs for gtfs-csv-validator


import os as os
import re as re
import gcv_support as gcvsup

def run_tests(data_type, schema_version, dir_path, con):
    print("TEST: Running tests")

    # create all tables for this particular data_type
    gcvsup.create_schema_tables(data_type, schema_version, con)

    print("in run_tests 1")

    # read all files from directory test_files/data_schema/version
    file_list = os.listdir(path = dir_path)

    print("in run_tests 2")

    for file_name in file_list:
        print("TEST: Testing file " + file_name)
        # check schema
        # loads file_name into schema_table checks for errors

         # data_type is pathways, flex or osw
        # pathways tables are levels_schema, pathways_schema, stops_schema 
        if(data_type == 'gtfs_pathways'):
            if(re.search('levels', file_path, re.IGNORECASE) != None):  
                schema_table = 'levels'
                file_table = 'levels_file'
            elif(re.search('pathways', file_path, re.IGNORECASE) != None):  
                schema_table = 'pathways'
                file_table = 'pathways_file'
            elif(re.search('stops', file_path, re.IGNORECASE) != None):  
                schema_table = 'stops'
                file_table = 'stops_file'
            else:
                raise AssertionError('file name expected to contain levels, pathways or stops for gtfs_pathways')
        
        # file_path, data_type, con
        file_path = dir_path + '/' + file_name
        gcvsup.check_schema(file_path, schema_table, file_table, con)
        print("") # add space after testing for file is done

    gcvsup.check_rules(data_type, file_name, con)

    # when all tests are done, drop tuples from schema tables and file tables
    cur = con.cursor()
    cur.execute("drop table levels")
    cur.execute("drop table pathways")
    cur.execute("drop table stops")
    cur.execute("drop table levels_file")
    cur.execute("drop table pathways_file")
    cur.execute("drop table stops_file")






