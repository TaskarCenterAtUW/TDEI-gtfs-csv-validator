This is intended to be a framework for a gtfs file validator for TDEI project

## Code structure
The structure is that the gtfs csv files are read into a sqlite database - the load into
the db does some of the schema checking. The load into the db is followed by running a set of sql
queries which do an additional set of checks.

## Validate a file
To validate a file, edit the gcv_main.py file with the appropriate data_type, schema_version and
test_dirs as instructed in the file. The script is currently set up to validate the mbta_20220920 files.

When validating your own files:
put the files you want to validate in a directory, or create a set of directories you want to test, each directory should contain a pathways 'release' or a flex 'release' 

For pathways, the script expects the directory to contain levels, pathways and stops files

For flex, the script expects the directory to contain booking_rules, location_groups and stop_times files

Test files are provided in the test_files directory

Edit gcv_main.py to set the variables:
    data_type = 'gtfs_pathways' (or 'gtfs_flex' )
    schema_version = 'v1.0' (for pathways) (or 'v2.0' for flex)
    test_dirs = ['path to dir 1', 'path to dir 2', ...]

then execute main.py

results and some logging are printed to the console

## Test the script
This package also contains tests to test the script. There are two primary sets of tests - test_flex.py and test_pathways.py for flex and pathways respectively. Execute either of those files (without modification) to run those tests. 

## Adding a test release
To add a flex or pathways release to be used to test the script, go to the appropriate directory under test_files and add a directory with the appropriate files. Then edit the test script to add that directory to the test.

## Adding a test
To add a test - for example - a new pathways or flex requirement, go rules and edit the appropriate file and add a rule name, a message to be printed when the test fails and a sql query for the test. If the sql query returns anything other than 'None' the test will be
marked as failing.

## Adding a new file type
If you wish to add a new flex or pathways file type, go to schemas and add a file
describing the new files. Columns used are: FieldName, Type, Required (from GTFS spec), sqliteType. FieldName, Type and Required are to be taken from the GTFS spec, the sqliteType 
is a string that creates an attribute of the appropriate type in sqllite