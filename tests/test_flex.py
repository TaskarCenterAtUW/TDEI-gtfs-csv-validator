# test the gtfs-csv-validator with gtfs-flex files

import test_support

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

# set the params here until I learn how to add params to a python function
data_type = 'gtfs_flex' 
schema_version = 'v2.0' 

test_dirs = ['tests/test_files/gtfs_flex/v2.0/success_1_all_attrs']
#test_dirs = ['tests/test_files/gtfs_flex/v2.0/fail_schema_1']

test_support.test_dir(data_type, schema_version, test_dirs)

