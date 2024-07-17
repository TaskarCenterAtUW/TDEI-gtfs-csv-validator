 # support functions for testing
 

# find the module... is one directory up
from pathlib import Path
import sys 

cur_path = Path(__file__)
mod_path = cur_path.parents[1]
sys.path.append(str(mod_path))

import re as re
from tcat_gtfs_csv_validator import gcv_test_release
from tcat_gtfs_csv_validator import exceptions as gcvex

def test_releases(data_type, schema_version, test_paths):

    count_int = 1
    for test_path in test_paths:
        count = str(count_int)  
        print("BEGIN TEST " + count + ": Calling run_tests on " + str(test_path))
        expect_success = True
        if(re.search('Fail', test_path, re.IGNORECASE) != None):
            expect_success = False; # if Fail, fail, or FAIL in file name
    
        try:
            gcv_test_release.test_release(data_type, schema_version, test_path)
        except gcvex.GCVError as err:
            if expect_success == False:
                print("END TEST " + count + ": [OK] Test Failed as expected. Error message:")
                print(str(err)) #raise
                print("\n")
            else:
                print("END TEST " + count + ":[FAIL] Test Failed unexpectedly. Error message:")
                print(str(err)) #raise
                print("\n")
        else: # if no exceptions
            print("END TEST " + count + ":[OK] Test Succeeded\n\n")
        count_int = count_int + 1


# this function takes the name of the test and the file name and
# checks to see if the file is expected to fail or pass this test
# returns yes if success is expected, no if file is expected to fail
# the test
def check_expect_success(test_name, file_name):
    # expect fail if we have Fail, fail or FAIL and the test name in the file name
    if(re.search('Fail', file_name, re.IGNORECASE) != None and 
        re.search(test_name, file_name) != None):
            return False; # if Fail, fail, or FAIL in file name
    return True

