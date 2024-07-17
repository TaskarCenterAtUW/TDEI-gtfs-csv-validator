# test the gtfs-csv-validator with gtfs-flex files

import test_support
from tcat_gtfs_csv_validator import gcv_test_release
from tcat_gtfs_csv_validator import exceptions as gcvex

# Use of script: Test a release - specify data_type, schema_version
# and a (list of) test directories 

# script params
# data_type = 'gtfs_flex' to test flex
# schema_version = version of schema to be tested against 
#        use v1.0 for pathways tests or v2.0 for flex tests
# test_paths = a list of paths to be tested, each path is expect to be
#             a directory or zipfile. The directory or zipfile 
#             is expected to contain a release for the data_type 
#             specified. gtfs_pathways expects levels, pathways and 
#             stops files. gtfs_flex expects booking_rules, loction_groups
#             and stop_times files

# set the params here until I learn how to add params to a python function
data_type = 'gtfs_flex' 
schema_version = 'v2.0' 

test_paths = ['tests/test_files/gtfs_flex/v2.0/success_1_all_attrs',
              'tests/test_files/gtfs_flex/v2.0/fail_schema_1',
              'tests/test_files/gtfs_flex/v2.0/success_1_all_attrs.zip',
              'tests/test_files/gtfs_flex/v2.0/fail_schema_1.zip']

test_support.test_releases(data_type, schema_version, test_paths)

