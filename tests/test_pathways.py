# test the gtfs-csv-validator with gtfs-pathways files

import test_support

# Use of script: Test a release - specify data_type, schema_version
# and a (list of) test directories 

# script params
# data_type = 'gtfs_pathways' to test pathways
# schema_version = version of schema to be tested against 
#        use v1.0 for pathways tests or v2.0 for flex tests
# test_paths = a list of paths to be tested, each path can be a directory
#             or a zip file. The directory or zip file 
#             is expected to contain a release for the data_type 
#             specified. gtfs_pathways expects levels, pathways and 
#             stops files. gtfs_flex expects booking_rules, loction_groups
#             and stop_times files

# set the params for the tests here 
data_type = 'gtfs_pathways' 
schema_version = 'v1.0' 

test_paths = ['tests/test_files/gtfs_pathways/v1.0/success_1_all_attrs',
              'tests/test_files/gtfs_pathways/v1.0/success_2_missing_attrs',
              'tests/test_files/gtfs_pathways/v1.0/fail_schema_1',
              'tests/test_files/gtfs_pathways/v1.0/mbta_20220920_small',
              'tests/test_files/gtfs_pathways/v1.0/mbta_20220920',
              'tests/test_files/gtfs_pathways/v1.0/fail_rules_1',
              'tests/test_files/gtfs_pathways/v1.0/success_1_all_attrs.zip',
              'tests/test_files/gtfs_pathways/v1.0/fail_rules_1.zip']

test_support.test_releases(data_type, schema_version, test_paths)


