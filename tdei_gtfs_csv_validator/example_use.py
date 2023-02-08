# simple example of the use of the gcv validator
 
from tdei_gtfs_csv_validator import gcv_test_release
from tdei_gtfs_csv_validator import exceptions as gcvex 

data_type = 'gtfs_pathways'
schema_version = 'v1.0'
#path = 'PUT PATH TO ZIP FILE OR DIRECTORY HERE'
path = '/Users/kristintufte/Projects/test-package/mytests/test_files/gtfs_pathways/v1.0/success_1_all_attrs.zip'

print("simple_test: trying calling test_release")

try:
    gcv_test_release.test_release(data_type, schema_version, dir_path)
except gcvex.GCVError as err:
    print("Test Failed\n")
    print(err) 
else: # if no exceptions
    print("Test Succeeded")