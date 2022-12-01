# test fncs for gtfs-csv-validator


import os as os
import re as re
import gcv_support as gcvsup

def run_tests(data_type, schema_version, dir_path, con):
    #print("TEST: begin run_tests")

    # create all tables for this particular data_type
    gcvsup.create_schema_tables(data_type, schema_version, con)

    # read all files from directory test_files/data_schema/version
    file_list = os.listdir(path = dir_path)

    fail = False
    for file_name in file_list:
        print("TEST: Testing file: " + file_name)
        # check schema
        # loads file_name into schema_table checks for errors

         # data_type is pathways, flex or osw
        # pathways tables are levels_schema, pathways_schema, stops_schema 
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
            else:
                raise AssertionError('file name expected to contain levels, pathways or stops for gtfs_pathways')
        
        # file_path, data_type, con
        file_path = dir_path + '/' + file_name
        fail = False
        try:
            gcvsup.check_schema(file_path, schema_table, file_table, con)
        except:
            fail = True
        print("") # add space after testing for file is done
    
    if(fail == True):
        gcvsup.drop_all_tables(data_type, con)
        raise RuntimeError("schema check failed, see trace messages")    

    print("checking " + data_type + " rules on " + dir_path)
    try:
        gcvsup.check_rules(data_type, schema_version, con)
    except:
        gcvsup.drop_all_tables(data_type, con)
        raise RuntimeError("rules check failed, see trace messages")

    # for now print out the tables...
    #gcvsup.print_schema_tables(data_type, con)
    gcvsup.drop_all_tables(data_type, con)






