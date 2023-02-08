This package can be used to validate GTFS CSV files. It is
focused on GTFS-Pathways and GTFS-Flex files. 

## Installing the Package
First, create and activate a virtual environment:
python3 -m venv your-folder-name
cd your-folder-name
source bin/activate

Then install the package from test pypi:
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps TDEI-gtfs-csv-validator==0.0.26

you should get version 0.0.26

also: https://test.pypi.org/project/tdei-gtfs-csv-validator/0.0.26/

install dependencies:
I could not get pip to install dependencies, so grab requirements.txt from the github repo and use pip
to install the requirements in your venv

pip3 install -r requirements.txt

https://github.com/TaskarCenterAtUW/TDEI-gtfs-csv-validator/blob/master/requirements.txt


Package is now installed.

## Using tdei_gtfs_csv_validator
The primary function in this package is test_release. A GTFS release
is a set of GTFS files. This code will test GTFS-Flex and GTFS-Pathways
releases. The tests focus on the flex- and pathways-specific files (for now).

### Summary
The primary function in this package is test_release. An example of using
this function is provided in the file example_use.py which is included in the release.
Replace the placedholder with a path to a directory or zip file containing a GTFS
release and run the script. The code from this script is below as well.

Sample good and bad GTFS-Pathways and GTFS-Flex files can be found in the project
github repo in tests/test_files. Here is a link to some pathways files:

https://github.com/TaskarCenterAtUW/TDEI-gtfs-csv-validator/tree/master/tests/test_files/gtfs_pathways/v1.0

Suggest:
mkdir test_dir
cd test_dir
copy the code below into a file example_use.py
download a pathways release (directory or zip file from the above)
replace placeholder in code with path to the release you just downloaded
python3 example_use.py to run it

## simple example of the use of the gcv validator

example_use.py

from tdei_gtfs_csv_validator import gcv_test_release
from tdei_gtfs_csv_validator import exceptions as gcvex

data_type = 'gtfs_pathways'
schema_version = 'v1.0'
path = 'PUT PATH TO ZIP FILE OR DIRECTORY HERE'

print("simple_test: trying calling test_release")

try:
    gcv_test_release.test_release(data_type, schema_version, path)
except gcvex.GCVError as err:
    print("Test Failed\n")
    print(err)
else: # if no exceptions
    print("Test Succeeded")


## Details
A GTFS releaseis a set of GTFS files. This code will test GTFS-Flex and GTFS-Pathways
releases. The tests focus on the flex- and pathways-specific files (for now).

### Using the test_release function
Call the test_release function to test a GTFS release. The GTFS release is
expected to be a directory which contains the flex or pathways release files
or a zip file containing the release.  
For pathways, the script expects the release to contain levels, pathways and stops files. For flex, the script expects the release to contain booking_rules, location_groups and stop_times files.

To validate your own release, put the files for the release that you want to validate in a directory or zip file and then use test_release as follows:

Parameters to test_release are:
    data_type = 'gtfs_pathways' or 'gtfs_flex' 
    schema_version = 'v1.0' (for pathways) or 'v2.0' (for flex)
    input_path = path to directory or zip file containing the release 

Test files are provided in the test_files directory which can be used for referece or in testing the script below.

## Testing the script
Tests for the scripts are available in the github repo. There are two primary sets of tests - tests to test flex releases (test_flex.py) and tests to test pathways releases (test_pathways.py). These tests use the files which can be found in the test_files subdirectory of the tests directory. You can run without modification or modify to test different files.  

###To use the tests:
clone from this repo: https://github.com/TaskarCenterAtUW/TDEI-gtfs-csv-validator
create and activate a virtual environment
install dependencies from requirements.txt
then run either test_flex.py or test_pathways.py - they should run without modification - they are a bit finicky about what directory you run them from, but other than that should work

## Code structure
The structure is that the gtfs csv files are read into a sqlite database - the load into
the db does some of the schema checking. The load into the db is followed by running a set of sql
queries which do an additional set of checks.

## Adding tests 
### Adding a new release to be used in testing the scripts
To add a flex or pathways release to be used to test the script (note a release is a set of GTFS files), go to the appropriate directory under test_files and add a directory with the appropriate files. Then edit the appropriate test script to add that directory to the test.

### Adding a new rule to be tested 
To add a new rule to be tested test - for example - if you want to add a new pathways or flex requirement, go rules and edit the appropriate file and add a rule name, a message to be printed when the test fails and a sql query for the test. The sql query should be written so that if the sql query returns anything other than 'None' the test will be marked as failing.

### Adding a new type of file to ber tested
If you wish to add a new flex or pathways file type to be tested - the current code tests only the Flex and Pathways-specific files, so tests for other files in the GTFS spec need to be added. To do so, go to the gtfs_flex or gtfs_pathways directory in the schemas directory and add a file describing the new file. Columns you will need are are: FieldName, Type, Required (from GTFS spec), sqliteType. FieldName, Type and Required are to be taken from the GTFS spec, the sqliteType is a string that creates an attribute of the appropriate type in sqllite


## TODOs
gcv_test_release should function as command line (it doesn't right now)

works on directories not on zip files - needs to be changed