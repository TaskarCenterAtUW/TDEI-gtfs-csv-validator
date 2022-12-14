This is intended to be a framework for a gtfs file validator for TDEI project

The structure is that the gtfs csv files are read into a sqlite database - the load into
the db does some of the schema checking. The load into the db is followed by running a set of sql
queries which do an additional set of checks.

You may run this script with a set of provided test files or with your own files.

To run with provided test files: 
The script is set up to run with the mbta files - you can just execute
main.py and it will test the mbta_20220920 files.

To test with other test files, simply edit the data_type, schema_version and test_dirs attributes in main.py as specified
in the comments in main.py.

To test your own files:
put the files you want to test in a directory, or create a set of directories you want to test, each directory should contain a pathways 'release' or a flex 'release' 

For pathways, the script expects the directory to contain levels, pathways and stops files

For flex, the script expects the directory to contain booking_rules, location_groups and stop_times files

Test files are provided in the test_files directory

Edit main.py to set the variables:
    data_type = 'gtfs_pathways' (or 'gtfs_flex' )
    schema_version = 'v1.0' (for pathways) (or 'v2.0' for flex)
    test_dirs = ['path to dir 1', 'path to dir 2', ...]

then execute main.py

results and some logging are printed to the console
