# test the gtfs-csv-validator with gtfs-pathways files

# TODO don't like this, but couldn't figure out how to make the paths work
import sys
sys.path.append(".")

from tdei_gtfs_csv_validator import gcv_runtests
import sqlite3 as sql

# Use of script: Test a release - specify data_type, schema_version
# and a (list of) test directories 

# script params
# data_type = 'gtfs_flex' to test flex
# schema_version = version of schema to be tested against 
#        use v1.0 for pathways tests or v2.0 for flex tests
# test_dirs = a list of directories to be tested, each directory 
#             is expected to contain a release for the data_type 
#             specified. gtfs_pathways expects levels, pathways and 
#             stops files. gtfs_flex expects booking_rules, loction_groups
#             and stop_times files

# set the params for the tests here 
data_type = 'gtfs_pathways' 
schema_version = 'v1.0' 

#test_dirs = ['tests/test_files/gtfs_pathways/v1.0/success_1_all_attrs',
#             'tests/test_files/gtfs_pathways/v1.0/success_2_missing_attrs',
#             'tests/test_files/gtfs_pathways/v1.0/fail_schema_1']


#test_dirs = ['tests/test_files/gtfs_pathways/v1.0/success_1_all_attrs']
#test_dirs = ['tests/test_files/gtfs_pathways/v1.0/success_2_missing_attrs']
#test_dirs = ['tests/test_files/gtfs_pathways/v1.0/fail_schema_1']
#test_dirs = ['tests/test_files/gtfs_pathways/v1.0/mbta_20220920_small']
test_dirs = ['tests/test_files/gtfs_pathways/v1.0/mbta_20220920']

# set up sqlite connection
# create a temp db in RAM
# schemas are stored in csv files for clarity and ease of maintenance
con = sql.connect(':memory:') 
cur = con.cursor()

for dir_path in test_dirs:  
    print("Calling run_tests on " + dir_path)
    try:
        gcv_runtests.run_tests(data_type, schema_version, dir_path, con)
    except Exception as err:
        print("TEST FAILED")
        print(err)
    else:
        print("TEST SUCCEEDED - ALL DONE")

con.close()




